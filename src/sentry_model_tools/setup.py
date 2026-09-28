from setuptools import find_packages, setup


setup(
    name="sentry_model_tools",
    version="0.1.0",
    packages=find_packages(),
    package_data={
        "xmacro": ["*.xmacro"],
        "sdformat_tools": ["*.xmacro"],
    },
    data_files=[
        (
            "share/ament_index/resource_index/packages",
            ["resource/sentry_model_tools"],
        ),
        ("share/sentry_model_tools", ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="gzu-prink",
    maintainer_email="agr.thu23@gzu.edu.cn",
    description="Workspace-local xmacro and SDF-to-URDF tools for the sentry model.",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "xmacro4sdf = sdformat_tools.xmacro4sdf:xmacro4sdf_main",
            "sdf2urdf = sdformat_tools.sdf2urdf:sdf2urdf_main",
        ],
    },
)
