#!/bin/bash
curl http://localhost:8000/health || exit 1
curl http://localhost:8000/tabular/health || exit 1