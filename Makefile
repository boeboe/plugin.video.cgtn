default: clean package

clean:
	rm plugin.video.cgtn-0.0.1.zip

package:
	cd .. ; zip plugin.video.cgtn/plugin.video.cgtn-0.0.1.zip -@ < plugin.video.cgtn/package.lst
