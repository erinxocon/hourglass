import asyncio
import aiodocker


async def list_things():
    docker = aiodocker.Docker()
    print("== Images ==")
    for image in await docker.images.list():
        tags = image["RepoTags"][0] if image["RepoTags"] else ""
        print(image["Id"], tags)
    print("== Containers ==")
    for container in await docker.containers.list():
        print(f" {container._id}")
    await docker.close()


async def run_container():
    docker = aiodocker.Docker()
    print("== Running a hello-world container ==")
    container = await docker.containers.create_or_replace(
        config={
            "Cmd": ["/bin/ash", "-c", 'echo "hello world"'],
            "Image": "alpine:latest",
        },
        name="testing",
    )
    await container.start()
    logs = await container.log(stdout=True)
    print("".join(logs))
    await container.delete(force=True)
    await docker.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(list_things())
    loop.run_until_complete(run_container())
    loop.close()