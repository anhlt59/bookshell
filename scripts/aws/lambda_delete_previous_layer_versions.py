import boto3

client = boto3.client("lambda")


def list_layers(name_prefix=None, runtime=None):
    response = client.list_layers(CompatibleRuntime=runtime)
    for item in response.get("Layers", []):
        if name_prefix and name_prefix not in item["LayerName"]:
            continue
        print(item["LayerName"], item["LatestMatchingVersion"]["Version"])
        yield item["LayerName"]


def delete_layer_versions(layer_name=None, max_retain=5):
    response = client.list_layer_versions(LayerName=layer_name)
    versions = sorted([item["Version"] for item in response["LayerVersions"]])

    if len(versions) > max_retain:
        for version in versions[: len(versions) - max_retain]:
            print(f"delete layer version: {layer_name}:{version}")
            client.delete_layer_version(LayerName=layer_name, VersionNumber=version)


def main():
    layers = list_layers("materially-testing", "nodejs")
    for layer in layers:
        delete_layer_versions(layer)


main()
