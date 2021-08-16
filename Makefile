PY = python3
SHELL = zsh
FILTER = hip21-ocrevaluation list
PARSER = hip21-ocrevaluation parse
WRITER = hip21-ocrevaluation join

# Set to --excel to output Excel instead of CSV
WRITER_OPTIONS = --csv

RM = rm -f

TEMP_CSV =  \
	temp/enp.ocrevalCER.csv \
	temp/enp.ocrevalWER.csv \
	temp/impact.ocrevalCER.csv \
	temp/impact.ocrevalWER.csv \
	temp/enp.conf.csv \
	temp/impact.conf.csv \
	temp/enp.dinglehopper.csv \
	temp/impact.dinglehopper.csv \
	temp/impact.ocrevalUAtion.csv \
	temp/enp.ocrevalUAtion.csv \
	temp/enp.LayoutEval.csv \
	temp/impact.LayoutEval.csv \
	temp/impact.primaCER.csv \
	temp/impact.primaWER.csv \
	temp/impact.primaFCER.csv \
	temp/impact.primaBoW.csv \
	temp/enp.primaCER.csv \
	temp/enp.primaBoW.csv \
	temp/enp.primaWER.csv \
	#temp/texteval-enp-fcer/csv \

# BEGIN-EVAL makefile-parser --make-help Makefile

help:
	@echo ""
	@echo "  Targets"
	@echo ""
	@echo "    temp    Build all the CSV"
	@echo "    excel  Build big excel table"
	@echo ""
	@echo "  Variables"
	@echo ""
	@echo "    WRITER_OPTIONS  Set to --csv to output CSV instead of Excel"

# END-EVAL

# Install the script with pip
install:
	pip install .

# Build all the intermediate CSV
temp: $(TEMP_CSV)

temp/enp.ocrevalCER.csv:
	$(PARSER) ocrevalCER $@ $$($(FILTER) enp ocrevalCER)
temp/impact.ocrevalCER.csv:
	$(PARSER) ocrevalCER $@ $$($(FILTER) impact ocrevalCER)

temp/enp.ocrevalWER.csv:
	$(PARSER) ocrevalWER $@ $$($(FILTER) enp ocrevalWER)
temp/impact.ocrevalWER.csv:
	$(PARSER) ocrevalWER $@ $$($(FILTER) impact ocrevalWER)

temp/enp.dinglehopper.csv:
	$(PARSER) dinglehopper $@ $$($(FILTER) enp dinglehopper)
temp/impact.dinglehopper.csv:
	$(PARSER) dinglehopper $@ $$($(FILTER) impact dinglehopper)

temp/impact.ocrevalUAtion.csv:
	$(PARSER) ocrevalUAtion $@ $$($(FILTER) impact ocrevalUAtion)
temp/enp.ocrevalUAtion.csv:
	$(PARSER) ocrevalUAtion $@ $$($(FILTER) enp ocrevalUAtion)

temp/impact.conf.csv:
	$(PARSER) conf $@ $$($(FILTER) impact conf)
temp/enp.conf.csv:
	$(PARSER) conf $@ $$($(FILTER) enp conf)

temp/impact.LayoutEval.csv:
	$(PARSER) LayoutEval $@ $$($(FILTER) enp LayoutEval)
temp/enp.LayoutEval.csv:
	$(PARSER) LayoutEval $@ $$($(FILTER) enp LayoutEval)

temp/impact.primaCER.csv:
	$(PARSER) texteval $@ CER prima-texteval/impact.primaCER.csv
temp/impact.primaFCER.csv:
	$(PARSER) texteval $@ FCER prima-texteval/impact.primaFCER.csv
temp/impact.primaWER.csv:
	$(PARSER) texteval $@ WER prima-texteval/impact.primaWER.csv
temp/impact.primaBoW.csv:
	$(PARSER) texteval $@ BoW prima-texteval/impact.primaBoW.csv

# TODO
#csv/texteval-enp-cer.csv:
	#$(PARSER) texteval --dataset-prefix enp --first-only $@ CER eval/prima_texteval/*primaCER.csv eval/prima_texteval/texteval/*primaCER.csv eval-enp-missing/*primaCER* eval-dummy-prima/*.csv missing_final/*primaCER*
#csv/texteval-enp-wer.csv:
	#$(PARSER) texteval --dataset-prefix enp --first-only $@ WER eval/prima_texteval/*primaWER.csv eval/prima_texteval/texteval/*primaWER.csv eval-enp-missing/*primaWER* missing_final/*primaWER*
#csv/texteval-enp-bow.csv:
	#$(PARSER) texteval --dataset-prefix enp --first-only $@ BOW eval/prima_texteval/*primaBoW.csv eval/prima_texteval/texteval/*primaBoW.csv eval-enp-missing/*primaBoW* missing_final/*primaBoW*
#csv/texteval-enp-fcer.csv:
	#$(PARSER) texteval --dataset-prefix enp --first-only $@ FCER eval/prima_texteval/*primaFCER.csv eval/prima_texteval/texteval/*primaBoW.csv eval-enp-missing/*primaBoW*

clean:
	$(RM) temp
	$(RM) eval.csv*

# Build big excel table
excel:
	$(PY) $(WRITER) $(WRITER_OPTIONS) eval.xlsx > invalid-values.txt

# TODO
#dummy-oom-data:
	#bash ./generate-prima-oom-dummy-csv.sh
