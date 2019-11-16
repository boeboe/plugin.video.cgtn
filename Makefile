default: clean package

clean:
	rm -f plugin.video.cgtn-0.0.2.zip

package:
	cd .. ; zip plugin.video.cgtn/plugin.video.cgtn-0.0.2.zip -@ < plugin.video.cgtn/package.lst ; cp plugin.video.cgtn/plugin.video.cgtn-0.0.2.zip ~/
