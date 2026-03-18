#!/usr/bin/env bash
alembic revision --autogenerate -m "${1:-init}"
