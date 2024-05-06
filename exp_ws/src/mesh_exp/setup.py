from setuptools import setup

package_name = 'mesh_exp'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lchovet',
    maintainer_email='loick.chovet@uni.lu',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pc_data = mesh_exp.pc_data:main',
            'pc_logger = mesh_exp.pc_logger:main',
            'byte_sender = mesh_exp.byte_sender:main',
            'byte_logger = mesh_exp.byte_logger:main',
        ],
    },
)
