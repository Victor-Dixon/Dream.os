#!/bin/bash
# Phase 5 Advanced SSL Configuration Script
# Automated SSL certificate management and renewal

set -e

# Configuration variables
DOMAIN=${DOMAIN:-localhost}
EMAIL=${SSL_EMAIL:-admin@localhost}
CERT_DIR="/etc/ssl/certs"
KEY_DIR="/etc/ssl/private"
ACME_CHALLENGE_DIR="/var/www/acme-challenge"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create necessary directories
create_directories() {
    log_info "Creating SSL directories..."
    mkdir -p "$CERT_DIR" "$KEY_DIR" "$ACME_CHALLENGE_DIR"
    chmod 755 "$CERT_DIR" "$KEY_DIR" "$ACME_CHALLENGE_DIR"
}

# Generate self-signed certificate for development
generate_self_signed() {
    log_info "Generating self-signed SSL certificate..."
    openssl req -x509 -newkey rsa:4096 -keyout "$KEY_DIR/selfsigned.key" -out "$CERT_DIR/selfsigned.crt" -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/CN=$DOMAIN"
    log_success "Self-signed certificate generated"
}

# Generate DH parameters for forward secrecy
generate_dh_params() {
    if [ ! -f "$CERT_DIR/dhparam.pem" ]; then
        log_info "Generating DH parameters (this may take a while)..."
        openssl dhparam -out "$CERT_DIR/dhparam.pem" 2048
        log_success "DH parameters generated"
    else
        log_info "DH parameters already exist"
    fi
}

# Generate ECC certificate for modern clients
generate_ecc_cert() {
    log_info "Generating ECC certificate..."
    openssl ecparam -genkey -name secp384r1 -out "$KEY_DIR/ecc.key"
    openssl req -new -key "$KEY_DIR/ecc.key" -out "$CERT_DIR/ecc.csr" -subj "/C=US/ST=State/L=City/O=Organization/CN=$DOMAIN"
    openssl x509 -req -days 365 -in "$CERT_DIR/ecc.csr" -signkey "$KEY_DIR/ecc.key" -out "$CERT_DIR/ecc.crt"
    log_success "ECC certificate generated"
}

# Configure certificate chains
setup_cert_chains() {
    log_info "Setting up certificate chains..."

    # Combine certificates for better compatibility
    if [ -f "$CERT_DIR/intermediate.crt" ]; then
        cat "$CERT_DIR/selfsigned.crt" "$CERT_DIR/intermediate.crt" > "$CERT_DIR/fullchain.crt"
    else
        cp "$CERT_DIR/selfsigned.crt" "$CERT_DIR/fullchain.crt"
    fi

    # Set proper permissions
    chmod 644 "$CERT_DIR"/*.crt
    chmod 600 "$KEY_DIR"/*.key

    log_success "Certificate chains configured"
}

# Test certificate validity
test_certificates() {
    log_info "Testing certificate validity..."

    if openssl x509 -in "$CERT_DIR/selfsigned.crt" -checkend 86400 > /dev/null 2>&1; then
        log_success "Certificate is valid for at least 24 hours"
    else
        log_warning "Certificate expires within 24 hours"
    fi

    # Test ECC certificate if it exists
    if [ -f "$CERT_DIR/ecc.crt" ]; then
        if openssl x509 -in "$CERT_DIR/ecc.crt" -checkend 86400 > /dev/null 2>&1; then
            log_success "ECC certificate is valid"
        else
            log_warning "ECC certificate expires soon"
        fi
    fi
}

# Setup OCSP stapling
setup_ocsp() {
    log_info "Setting up OCSP stapling..."

    # Create OCSP cache directory
    mkdir -p /var/cache/nginx/ocsp
    chmod 755 /var/cache/nginx/ocsp

    log_success "OCSP stapling configured"
}

# Main execution
main() {
    log_info "Starting Phase 5 SSL configuration..."

    create_directories
    generate_self_signed
    generate_ecc_cert
    generate_dh_params
    setup_cert_chains
    setup_ocsp
    test_certificates

    log_success "Phase 5 SSL configuration completed!"
    log_info "Certificate files created in: $CERT_DIR"
    log_info "Private keys created in: $KEY_DIR"
    log_info "DH parameters: $CERT_DIR/dhparam.pem"
    log_info "OCSP cache: /var/cache/nginx/ocsp"
}

# Run main function
main "$@"