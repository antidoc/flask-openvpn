from OpenSSL import crypto
import sys, os
from ..config import org_fields

of = org_fields()

with open(of.CACERT, 'r') as file:
    cacert = crypto.load_certificate(crypto.FILETYPE_PEM, file.read())

with open(of.CAKEY, 'r') as file:
    cakey = crypto.load_privatekey(crypto.FILETYPE_PEM, file.read())

def make_key():
    pkey = crypto.PKey()
    pkey.generate_key(crypto.TYPE_RSA, 2048)
    return pkey


def make_csr(cn, pkey=make_key(), email=of.email, C=of.C, ST=of.ST, L=of.L, OU=of.OU, hashalgorithm='sha256WithRSAEncryption'):
    req = crypto.X509Req()
    req.get_subject().CN = cn
    req.get_subject().C = C
    req.get_subject().ST = ST
    req.get_subject().L = L
    req.get_subject().OU = OU
    req.get_subject().emailAddress = email
    req.set_pubkey(pkey)
    req.sign(pkey, hashalgorithm)
    return req


def create_new_certificate(csr, cakey, cacert, serial):
    cert = crypto.X509()
    cert.set_serial_number(serial)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(60*60*24*365*10)
    cert.set_issuer(cacert.get_subject())
    cert.set_subject(csr.get_subject())
    cert.set_pubkey(csr.get_pubkey())
    cert.set_version(2)

    extensions = []
    extensions.append(crypto.X509Extension(b'basicConstraints', False ,b'CA:FALSE'))

    extensions.append(crypto.X509Extension(b'subjectKeyIdentifier', False, b'hash', subject=cert))
    extensions.append(crypto.X509Extension(b'authorityKeyIdentifier', False, b'keyid:always,issuer:always', subject=cacert, issuer=cacert))

    cert.add_extensions(extensions)
    cert.sign(cakey, 'sha256WithRSAEncryption')

    return cert

def gen_cert(username, cacert = cacert, cakey=cakey, serial=0x0C):
    template = open('app/static/certs/template.ovpn', 'r')
    config_file = open('app/static/certs/' + username + '.ovpn', 'a+')
    key = make_key()
    csr = make_csr(username)
    crt = create_new_certificate(csr, cakey, cacert, serial)
    f_ca = crypto.dump_certificate(crypto.FILETYPE_PEM, cacert)
    f_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, key)
    f_cert = crypto.dump_certificate(crypto.FILETYPE_PEM, crt)
    config_file.write(template.read() + '\n<ca>\n' + f_ca.decode() + '</ca>\n<cert>\n' + f_cert.decode() + '</cert>\n<key>\n' + f_key.decode() + '</key>')
    config_file.close()
