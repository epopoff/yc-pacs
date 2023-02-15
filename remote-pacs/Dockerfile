FROM osimis/orthanc:latest

RUN pip3 install requests

COPY *.py /scripts/
COPY filter-http.lua /scripts/

ENV ORTHANC__LUA_SCRIPTS='["/scripts/filter-http.lua"]'