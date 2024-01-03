from digitalhub_core.client.builder import ClientBuilder, ClientDHCore, ClientLocal, client_builder, get_client


def test_client_builder():
    builder = ClientBuilder()

    # Test build method for local client
    local_client = builder.build(local=True)
    assert isinstance(local_client, ClientLocal)

    # Test build method for non-local client
    builder = ClientBuilder()  # create a new builder instance
    non_local_client = builder.build(local=False)
    assert isinstance(non_local_client, ClientDHCore)

    # Test that the same client instance is returned on subsequent calls to build
    same_client = builder.build(local=False)
    assert same_client is non_local_client


def test_get_client_local():
    # Test get_client method for local client
    local_client = get_client(local=True)
    assert isinstance(local_client, ClientLocal)

    # Reset client_builder instance
    client_builder._client = None


def test_get_client_non_local():
    # Test get_client method for non-local client
    non_local_client = get_client(local=False)
    assert isinstance(non_local_client, ClientDHCore)

    # Reset client_builder instance
    client_builder._client = None


def test_get_client_same_instance():
    # Test that the same client instance is returned on subsequent calls to get_client
    same_client = get_client(local=False)
    assert same_client is get_client(local=False)

    # Reset client_builder instance
    client_builder._client = None
