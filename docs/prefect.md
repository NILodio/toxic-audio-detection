# Developer Guide: Running Prefect Flows

This repository contains everything you need to run Prefect Server, a Prefect agent, or the Prefect CLI using Docker Compose. 

# Why Docker Compose?

There are a few reasons you might want to run Prefect using Docker Compose:
* You want to try Prefect without installing anything new on your workstation. 
* You are comfortable with Docker and prefer it over virtual environments or Anaconda. 
* You want to run Prefect on a system like CentOS 7 where installing Prefect dependencies is difficult.

# Prerequisites

* A Linux, MacOS, or Windows computer or VM with Docker installed. If you are running Windows, you must have Docker set up to use Linux containers, not Windows containers.

# Limitations

* If you run a Prefect agent in Docker, it will not be able to run `DockerContainer` deployments unless you share the host's Docker socket with the agent container because Docker-in-Docker is not supported. 

# Getting Started

The `docker-compose.yml` file contains five services:
* `database` - Postgres database for Prefect Server
* `minio` - MinIO S3-compatible object store, useful for experimenting with remote file storage without needing a cloud storage account.
* `server` - Prefect Server API and UI
* `agent` - Prefect Agent
* `cli` - A container that mounts this repository's `src` directory and offers an ideal environment for building and applying deployments and running flows. 
* `mlflow` - A container that mounts this repository's `src` directory and offers an ideal environment for running MLflow experiments and tracking runs.

## Developer Services
To run Prefect Server, open a terminal, navigate to the directory where you cloned this repository, and run:

```
docker-compose --profile develop up

make p-dev <-- detach run
```

This will start PostgreSQL, Prefect Server, Prefect Agent, Minio, Mlflow. When the serveris ready, you will see docker services:

```
toxic-audio-detection-server-1    | 
toxic-audio-detection-mlflow-1    | 
toxic-audio-detection-database-1  |
toxic-audio-detection-minio-1     |
toxic-audio-detection-agent-1     | 

```
## Prefect Server

The Prefect Server container shares port 4200 with the host machine, so if you open a web browser and navigate to `http://localhost:4200` you will see the Prefect UI.

## Prefect CLI

By default, the `cli` service doesn't run. It should be executed within a container that mounts the `src` subdirectory of this repository. This is useful for building, applying deployments, and running flows.

### Steps to run the CLI
Next, open another terminal in the same directory and run:

```
docker compose run cli

make cli
```

This runs an interactive Bash session in a container that shares a Docker network with the server you just started. If you run `ls`, you will see that the container shares the `src` subdirectory of the repository on the host machine:

```
root@fb032110b1c1:~/src#
```

To demonstrate the container is connected to the Prefect Server instance you launched earlier, run:

```
python src/flows/test.py
```

Then, in a web browser on your host machine, navigate to `http://localhost:4200/runs` and you will see the flow you just ran in your CLI container.

If you'd like to use the CLI container to interact with Prefect Cloud instead of a local Prefect Server instance, update `docker-compose.yml` and change the agent service's `PREFECT_API_URL` environment variable to match your Prefect Cloud API URL. Then, uncomment the `PREFECT_API_KEY` environment variable and replace `YOUR_API_KEY` with your own API key. If you'd prefer not to put your API key in a Docker Compose file, you can also store it in an environment variable on your host machine and pass it through to Docker Compose like so:

```
- PREFECT_API_KEY=${PREFECT_API_KEY}
```

## Prefect Agent

You can run a Prefect Agent by updating `docker-compose.yml` and changing `default` to match the name of the Prefect work queue you would like to connect to, and then running the following command:

```
docker-compose --profile agent up
```

This will run a Prefect agent and connect to the work queue you provided. 

As with the CLI, you can also use Docker Compose to run an agent that connects to Prefect Cloud by updating the agent's `PREFECT_API_URL` and `PREFECT_API_KEY` settings in `docker-compose.yml`.

## MinIO Storage

MinIO is an S3-compatible object store that works perfectly as remote storage for Prefect deployments. You can run it inside your corporate network and use it as a private, secure object store, or just run it locally in Docker Compose and use it for testing and experimenting with Prefect deployments. 



Although Prefect Server won't need to talk to MinIO, Prefect agents and the Prefect CLI will need to talk to both MinIO _and_ Prefect Server to create and run depoyments, so it's best to start them simultaneously.

After the MinIO container starts, you can load the MinIO UI in your web browser by navigating to `http://localhost:9000`. Sign in by entering `minioadmin` as both the username and password. 

Create a bucket named `prefect-flows` to store your Prefect flows, and then click **Identity->Service Accounts** to create a service account. This will give you an access key and a secret you can enter in a Prefect block to let the Prefect CLI and agents write to and read from your MinIO storage bucket.

After you create a MinIO service account, open the Prefect UI at `http://localhost:4200`. Click **Blocks**, then add a **Remote File System** block. Give the block any name you'd like, but remember what name you choose because you will need it when creating a deployment. 

In the *Basepath* field, enter `s3://prefect-flows`.

Finally, the *Settings* JSON field should look like this:

```
{
  "key": "YOUR_MINIO_KEY",
  "secret": "YOUR_MINIO_SECRET",
  "client_kwargs": {
    "endpoint_url": "http://minio:9000"
  }
}
```
Replace the placeholders with the key and secret MinIO generated when you created the service account. You are now ready to deploy a flow to a MinIO storage bucket! If you want to try it, open a new terminal and run:

```
docker compose run cli

make cli
```

Then, when the CLI container starts and gives you a Bash prompt, run:

```
prefect deployment build -sb "remote-file-system/your-storage-block-name" -n "Awesome MinIO deployment" -q "default" "test.py:greetings"
```

Now, if you open `http://localhost:9001/buckets/prefect-flows/browse` in a web browser, you will see that flow.py has been copied into your MinIO bucket.

## Next Steps

You can run as many profiles as once as you'd like. For example, if you have created a deployment and want to start and agent for it, but don't want to open two separate terminals to run Prefect Server, an agent, *and* MinIO you can start them all at once by running: 

```
docker compose --profile server --profile minio --profile agent up
```

And if you want to start two separate agents that pull from different work queues? No problem! Just duplicate the agent service, give it a different name, and set its work queue name. For example:

```
agent_two:
    image: prefecthq/prefect:2.3.0-python3.10
    restart: always
    entrypoint: ["prefect", "agent", "start", "-q", "YOUR_OTHER_WORK_QUEUE_NAME"]
    environment:
      - PREFECT_API_URL=http://server:4200/api
    profiles: ["agent"]
```
Now, when you run `docker-compose --profile agent up`, both agents will start, connect to the Prefect Server API, and begin polling their work queues.
