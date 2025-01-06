from flask import Flask, jsonify, request, abort
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.exceptions import InvalidSignature
import jwt
import datetime
import os
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Secure key storage (in a real scenario, use a proper key management system)
SECRET_KEY = os.urandom(32)
public_keys = {}

# Simulated scope-to-resource mapping
scope_resources = {
    "Ken": "Ken resource"
}

@app.route('/challenge', methods=['GET'])
def get_challenge():
    return jsonify({"challenge": os.urandom(32).hex()})

def verify_zkp(did, zkp, vc_claims, challenge):
    if did not in public_keys:
        return False
    public_key = public_keys[did]
    message = f"{vc_claims['access']}:{challenge}".encode()
    try:
        public_key.verify(
            bytes.fromhex(zkp),
            message,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False

@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.json
    if not data or 'did' not in data or 'zkp' not in data or 'vc_claims' not in data:
        abort(400, description="Missing required data")
    
    did = data['did']
    zkp = data['zkp']
    vc_claims = data['vc_claims']
    challenge = request.headers.get('X-Challenge')
    
    if not challenge:
        abort(400, description="Missing challenge header")
    
    if not verify_zkp(did, zkp, vc_claims, challenge):
        abort(401, description="ZKP verification failed")
    
    if 'access' not in vc_claims or vc_claims['access'] not in scope_resources:
        abort(403, description="Invalid or missing scope")
    
    token = jwt.encode({
        "sub": did,
        "scope": vc_claims['access'],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    }, SECRET_KEY, algorithm="HS256")
    
    return jsonify({"jwt": token})

@app.route('/token', methods=['POST'])
def get_token():
    data = request.json
    if not data or 'jwt' not in data:
        abort(400, description="Missing JWT")
    
    token = data['jwt']
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        scope = payload['scope']
        
        if scope in scope_resources:
            return jsonify({
                "access_token": os.urandom(16).hex(),
                "resource": scope_resources[scope]
            })
        else:
            abort(403, description="Invalid scope")
    except jwt.ExpiredSignatureError:
        abort(401, description="Token expired")
    except jwt.InvalidTokenError:
        abort(401, description="Invalid token")

@app.route('/register_key', methods=['POST'])
def register_key():
    data = request.json
    if not data or 'did' not in data or 'public_key' not in data:
        abort(400, description="Missing required data")
    
    did = data['did']
    public_key_pem = data['public_key']
    try:
        public_key = serialization.load_pem_public_key(public_key_pem.encode())
        public_keys[did] = public_key
        return jsonify({"message": "Public key registered successfully"})
    except ValueError:
        abort(400, description="Invalid public key format")

if __name__ == '__main__':
    app.run(ssl_context='adhoc', port=5000)
