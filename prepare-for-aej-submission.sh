#!/bin/bash
NAME=short-term-planning-replication
rm -f $NAME.zip
rm -f README.md
pandoc --to=markdown README.org >> README.md
cd ../
zip -r $NAME/$NAME.zip $NAME/README.md $NAME/env.yaml $NAME/single_agent_template.f90
zip $NAME/$NAME.zip $NAME/scripts/* -x $NAME/scripts/__pycache__/
zip $NAME/$NAME.zip $NAME/scripts/* -x $NAME/scripts/__pycache__/
zip $NAME/$NAME.zip $NAME/figures-tables/
zip $NAME/$NAME.zip $NAME/batch/*
zip $NAME/$NAME.zip $NAME/data/*
zip -r $NAME/$NAME.zip $NAME/models/*
zip -r $NAME/$NAME.zip $NAME/fortran/*/output*
zip $NAME/$NAME.zip $NAME/fortran/canonical_NK/time-posteriors/*
zip $NAME/$NAME.zip $NAME/fortran/finite_horizon_phibar/time-posteriors/*
cd $NAME
