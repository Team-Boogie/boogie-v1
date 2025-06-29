"""
This type stub file was generated by pyright.
"""

from typing import Any, TypedDict
from OpenSSL import SSL
from mitmproxy import certs, tls
from mitmproxy.proxy import context
from mitmproxy.proxy.layers import quic

logger = ...
_DEFAULT_CIPHERS = ...
_DEFAULT_CIPHERS_WITH_SECLEVEL_0 = ...
DEFAULT_HOSTFLAGS = ...
class AppData(TypedDict):
    client_alpn: bytes | None
    server_alpn: bytes | None
    http2: bool
    ...


def alpn_select_callback(conn: SSL.Connection, options: list[bytes]) -> Any:
    ...

class TlsConfig:
    """
    This addon supplies the proxy core with the desired OpenSSL connection objects to negotiate TLS.
    """
    certstore: certs.CertStore = ...
    def load(self, loader): # -> None:
        ...
    
    def tls_clienthello(self, tls_clienthello: tls.ClientHelloData): # -> None:
        ...
    
    def tls_start_client(self, tls_start: tls.TlsData) -> None:
        """Establish TLS or DTLS between client and proxy."""
        ...
    
    def tls_start_server(self, tls_start: tls.TlsData) -> None:
        """Establish TLS or DTLS between proxy and server."""
        ...
    
    def quic_start_client(self, tls_start: quic.QuicTlsData) -> None:
        """Establish QUIC between client and proxy."""
        ...
    
    def quic_start_server(self, tls_start: quic.QuicTlsData) -> None:
        """Establish QUIC between proxy and server."""
        ...
    
    def running(self): # -> None:
        ...
    
    def configure(self, updated): # -> None:
        ...
    
    def get_cert(self, conn_context: context.Context) -> certs.CertStoreEntry:
        """
        This function determines the Common Name (CN), Subject Alternative Names (SANs) and Organization Name
        our certificate should have and then fetches a matching cert from the certstore.
        """
        ...
    


