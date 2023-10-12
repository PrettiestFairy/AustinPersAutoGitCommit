FROM ubuntu:22.04
LABEL authors="austin"
ENV TZ=Asia/Shanghai
ENV GIT_USERNAME="AustinFairyland"
ENV GIT_EMAIL="fairylandhost@outlook.com"
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y openssh-client wget git tzdata && \
    RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    git config --global user.name $GIT_USERNAME && \
    git config --global user.email $GIT_EMAIL && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    /bin/bash /tmp/miniconda.sh -b -p /opt/conda 

RUN ssh-keygen -t ed25519 -C $GIT_EMAIL -f ~/.ssh/id_ed25519 -N "" && \
    eval "$(ssh-agent -s)" && \
    ssh-add ~/.ssh/id_ed25519 && \
    ssh-keyscan github.com >> ~/.ssh/known_hosts

ENV PATH /opt/conda/bin:$PATH
RUN conda create -n myenv python=3.9.13 && \
    echo "source activate myenv" > ~/.bashrc 

WORKDIR /application
ADD . /application
RUN /bin/bash -c "source activate myenv && pip install --no-cache-dir -r requirements.txt"
CMD ["/bin/bash", "-c", "cat ~/.ssh/id_ed25519.pub && source activate myenv && python run.py"]
