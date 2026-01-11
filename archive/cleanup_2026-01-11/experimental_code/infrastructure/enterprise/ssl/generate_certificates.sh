#!/bin/bash
# SSL Certificate Generation for Migrated Websites
# Generated: 2026-01-10 19:57:08

DOMAINS=(
    "crosbyultimateevents.com" "dadudekc.com" "tradingrobotplug.com" "weareswarm.online" "houstonsipqueen.com" "ariajet.site"
)

EMAIL="admin@tradingrobotplug.com"
CERT_PATH="/etc/letsencrypt/live"

echo "🔐 Generating SSL certificates for migrated websites..."

for domain in "${DOMAINS[@]}"; do
    echo "Processing $domain..."

    # Generate certificate
    sudo certbot certonly \
        --standalone \
        --agree-tos \
        --email $EMAIL \
        --domains $domain \
        --domains www.$domain \
        --non-interactive

    if [ $? -eq 0 ]; then
        echo "✅ Certificate generated for $domain"

        # Copy certificates to infrastructure
        sudo cp $CERT_PATH/$domain/fullchain.pem infrastructure\enterprise\ssl/certs/
        sudo cp $CERT_PATH/$domain/privkey.pem infrastructure\enterprise\ssl/private/

        # Set permissions
        sudo chmod 644 infrastructure\enterprise\ssl/certs/${domain}_fullchain.pem
        sudo chmod 600 infrastructure\enterprise\ssl/private/${domain}_privkey.pem
        sudo chown root:root infrastructure\enterprise\ssl/certs/* infrastructure\enterprise\ssl/private/*

        echo "✅ Certificates copied for $domain"
    else
        echo "❌ Failed to generate certificate for $domain"
    fi
done

echo "SSL certificate generation complete"
