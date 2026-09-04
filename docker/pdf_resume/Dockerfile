FROM necrux/alea-pdf-renderer:latest

ARG HTML
ARG MOUNT_POINT

COPY ${HTML} ${MOUNT_POINT}
RUN sed -i 's@<!-- H-ONLY -->.*<!-- /H-ONLY -->@@g' ${MOUNT_POINT}
