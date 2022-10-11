import os

from FileLocator import FileLocator
from KotsManifest import KotsManifest


class ChartVersion:
    __NON_FEATURE_BRANCHES = ('main', 'develop', 'development', 'master', 'release')
    __ORIGIN_BRANCH = str(os.getenv('GITHUB_REF'))

    def prepare_platform_commit(self) -> None:
        if self.__is_feature_branch():
            self.__update_chart_version()
        else:
            print(f"Workflow triggered by {self.__ORIGIN_BRANCH}. "
                  f"Creating commit without changes - using the 0.0.0-develop chartVersion.")

    def __is_feature_branch(self) -> bool:
        for branch in self.__NON_FEATURE_BRANCHES:
            if branch in self.__ORIGIN_BRANCH:
                return False

        return True

    def __update_chart_version(self):
        manifest_file = FileLocator.get_file_path(os.getenv('CHART_NAME'), "platform-deployment/manifests")
        KotsManifest(manifest_file).replace_develop_chart_tag_with_suffix()
