rmdir /S /Q dist
rmdir /S /Q build
rmdir /S /Q adamspy.egg-info
python setup.py sdist bdist_wheel
twine upload dist/*