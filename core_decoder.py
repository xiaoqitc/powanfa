import base64
import urllib.parse
import binascii
import re
import json
import html
import codecs
import jwt
import hashlib

# 检测Base64
def is_base64(s):
    try:
        return base64.b64encode(base64.b64decode(s)).decode() == s
    except Exception:
        return False

def decode_base64(s):
    try:
        return base64.b64decode(s).decode('utf-8')
    except Exception:
        return None

# 检测URL编码
def is_urlencode(s):
    return '%' in s

def decode_urlencode(s):
    try:
        return urllib.parse.unquote(s)
    except Exception:
        return None

# 检测Hex
def is_hex(s):
    try:
        bytes.fromhex(s)
        return True
    except Exception:
        return False

def decode_hex(s):
    try:
        return bytes.fromhex(s).decode('utf-8')
    except Exception:
        return None

# 检测JWT

def is_jwt(s):
    parts = s.split('.')
    return len(parts) == 3

def decode_jwt(s):
    try:
        header = jwt.get_unverified_header(s)
        payload = jwt.decode(s, options={"verify_signature": False})
        return json.dumps({'header': header, 'payload': payload}, ensure_ascii=False, indent=2)
    except Exception:
        return None

# 自动分析

def try_decode_base64(s):
    try:
        return base64.b64decode(s).decode('utf-8')
    except Exception:
        return None

def try_decode_base32(s):
    try:
        return base64.b32decode(s).decode('utf-8')
    except Exception:
        return None

def try_decode_base16(s):
    try:
        return base64.b16decode(s).decode('utf-8')
    except Exception:
        return None

def try_decode_url(s):
    try:
        return urllib.parse.unquote(s)
    except Exception:
        return None

def try_decode_hex(s):
    try:
        return bytes.fromhex(s).decode('utf-8')
    except Exception:
        return None

def try_decode_jwt(s):
    try:
        header = jwt.get_unverified_header(s)
        payload = jwt.decode(s, options={"verify_signature": False})
        return json.dumps({'header': header, 'payload': payload}, ensure_ascii=False, indent=2)
    except Exception:
        return None

def try_decode_html_entity(s):
    try:
        return html.unescape(s)
    except Exception:
        return None

def try_decode_rot13(s):
    try:
        return codecs.decode(s, 'rot_13')
    except Exception:
        return None

def try_decode_unicode_escape(s):
    try:
        return s.encode('utf-8').decode('unicode_escape')
    except Exception:
        return None

def try_recognize_md5(s):
    if re.fullmatch(r'[a-fA-F0-9]{32}', s):
        return '疑似MD5哈希值（无法逆向解密）'
    return None

def try_recognize_sha1(s):
    if re.fullmatch(r'[a-fA-F0-9]{40}', s):
        return '疑似SHA1哈希值（无法逆向解密）'
    return None

def try_recognize_sha256(s):
    if re.fullmatch(r'[a-fA-F0-9]{64}', s):
        return '疑似SHA256哈希值（无法逆向解密）'
    return None

# 支持的所有解码方式
DECODERS = [
    ("Base64", try_decode_base64),
    ("Base32", try_decode_base32),
    ("Base16", try_decode_base16),
    ("URL编码", try_decode_url),
    ("Hex", try_decode_hex),
    ("JWT", try_decode_jwt),
    ("HTML实体", try_decode_html_entity),
    ("ROT13", try_decode_rot13),
    ("Unicode转义", try_decode_unicode_escape),
    ("MD5识别", try_recognize_md5),
    ("SHA1识别", try_recognize_sha1),
    ("SHA256识别", try_recognize_sha256),
]

def brute_force_decode(s, max_depth=3, path=None, tried=None):
    if path is None:
        path = []
    if tried is None:
        tried = set()
    results = []
    for name, func in DECODERS:
        key = (name, s)
        if key in tried:
            continue
        tried.add(key)
        res = func(s)
        result = {
            'method': name,
            'input': s,
            'output': res if res is not None else '无法解码',
            'success': res is not None and not res.startswith('疑似'),
            'is_hash': res is not None and res.startswith('疑似'),
            'path': path + [name]
        }
        results.append(result)
        # 多层递归暴力解码
        if res and res != s and max_depth > 1 and result['success']:
            sub_results = brute_force_decode(res, max_depth-1, path + [name], tried)
            results.extend(sub_results)
    return results

def auto_analyze(text):
    candidates = re.findall(r'[A-Za-z0-9+/=\.%\-_]{8,}', text)
    all_results = []
    for c in set(candidates):
        decode_results = brute_force_decode(c, max_depth=3)
        # 先有数据（success=True），再哈希识别（is_hash=True），最后无数据
        decode_results_sorted = sorted(decode_results, key=lambda x: (not x['success'], not x['is_hash']))
        all_results.append({'original': c, 'decode_results': decode_results_sorted})
    return all_results 