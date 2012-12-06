from setuptools import setup, find_packages

setup(
        name='cmsplugin_image_gallery',
        version='1.1',
        description='Django cms plugin for insert images',
        packages = find_packages(),        
        install_requires = [
                              "Django>=1.4.1",
                              "django-cms",
                              "django-sekizai",
                              "PIL",
                              "easy-thumbnails >= 1.0",
                              "django-filer",    
                              "django-inline-ordering",
                            ],
        include_package_data=True,
        zip_safe=False,
)
