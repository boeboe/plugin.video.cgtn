RUNTEST2=python2 -m unittest discover -v -b
RUNTEST3=python3 -m unittest -v -b
ALLMODULES=$(patsubst %.py, %, $(wildcard test_*.py))
VERSION=0.0.4

.PHONY: tests_2 tests_3 clean package

default: clean package
tests: tests_2 tests_3

tests_2:
	${RUNTEST2} ${ALLMODULES}

tests_3:
	${RUNTEST3} ${ALLMODULES}

clean:
	rm -f plugin.video.cgtn-*.zip ; rm -rf ./build ./dist ./*.egg-info ./*/__pycache__ ./*/*.pyc

package:
	cd .. ; zip plugin.video.cgtn/plugin.video.cgtn-${VERSION}.zip -@ < plugin.video.cgtn/package.lst ; cp plugin.video.cgtn/plugin.video.cgtn-${VERSION}.zip ~/
