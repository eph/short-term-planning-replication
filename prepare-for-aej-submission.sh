#!/bin/bash
rm -f short-term-planning-replication.zip
pandoc --to=markdown README.org >> README.md
zip -r short-term-planning-replication.zip README.md env.yaml single_agent_template.f90
zip short-term-planning-replication.zip scripts/* -x scripts/__pycache__/
zip short-term-planning-replication.zip figures-tables
zip -r short-term-planning-replication.zip models/*
zip -r short-term-planning-replication.zip fortran/*/output*
zip  short-term-planning-replication.zip fortran/canonical_NK/time-posteriors/*
zip  short-term-planning-replication.zip fortran/finite_horizon_phibar/time-posteriors/*
