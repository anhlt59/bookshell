git clone https://github.com/OpenVPN/easy-rsa.git

cd easy-rsa/easyrsa3

./easyrsa init-pki
./easyrsa build-ca nopass
./easyrsa build-server-full vpn-materially.com nopass
./easyrsa build-client-full client.vpn-materially.com nopass

mkdir acm

cp pki/ca.crt acm
cp pki/issued/vpn-materially.com.crt acm
cp pki/issued/client.vpn-materially.com.crt acm
cp pki/private/vpn-materially.com.key acm
cp pki/private/client.vpn-materially.com.key acm

cd acm

aws acm import-certificate --certificate fileb://vpn-materially.com.crt --private-key fileb://vpn-materially.com.key --certificate-chain fileb://ca.crt --region us-east-1
aws acm import-certificate --certificate fileb://client.vpn-materially.com.crt --private-key fileb://client.vpn-materially.com.key --certificate-chain fileb://ca.crt --region us-east-1 