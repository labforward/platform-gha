import os

import ruamel.yaml


class KotsManifest:

    def __init__(self, manifest_file_path):
        self.manifest_file_path = manifest_file_path

    def replace_develop_chart_tag_with_suffix(self):
        manifest_yaml, file_stream = self.__get_manifest_yaml()
        self.__replace_develop_tag_with_suffix(manifest_yaml)
        self.__upload_manifest(manifest_yaml, file_stream)

    def __upload_manifest(self, data, yaml):
        with open(self.manifest_file_path, "w") as file:
            yaml.dump(data, file)

    def __get_manifest_yaml(self):
        yaml = ruamel.yaml.YAML()
        yaml.preserve_quotes = True
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.width = 300
        with open(self.manifest_file_path) as file:
            data = yaml.load(file)
        return data, yaml

    def __replace_develop_tag_with_suffix(self, manifest_yaml) -> None:
        new_version = self.__define_new_chart_version()
        manifest_yaml['spec']['chart']['chartVersion'] = new_version
        print(f"new chartVersion is {new_version}")

    def __define_new_chart_version(self) -> str:
        input_version = os.getenv('NEW_CHART_VERSION')
        if input_version == "":
            return self.short_commit_version()
        return input_version

    def short_commit_version(self):
        short_commit = str(os.getenv('GITHUB_SHA'))[:7]
        default_chart_version = f"0.0.0-{short_commit}"
        return default_chart_version
