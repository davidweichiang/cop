all: general.ics particular.ics

%.ics: %.csv
	python csv2ics.py < $< > $@
