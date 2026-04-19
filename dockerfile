FROM fedora:latest

RUN dnf -y install npx

RUN dnf -y install fedora-workstation-repositories && \
    dnf config-manager setopt google-chrome.enabled=1 && \
    dnf -y install google-chrome-stable && \
    dnf clean all

RUN npx @puppeteer/browsers install chrome-headless-shell@stable

RUN ln -sf $(find /chrome-headless-shell/ -type f -name chrome-headless-shell) /chrome-headless
