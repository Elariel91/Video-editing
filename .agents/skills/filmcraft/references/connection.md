# Connecting FilmCraft

Install FilmCraft and its CLI from the official upstream release instructions:
https://github.com/storytold/filmcraft#readme

Configure the agent client's MCP server with the actual absolute path to the installed `filmcraft-cli` executable. MCP registration is client configuration; adding this skill does not register a server or install the application.

For headless editing, launch the stdio server with:

```sh
filmcraft-cli mcp --project /absolute/path/to/project.fcproj
```

For a disposable demo session:

```sh
filmcraft-cli mcp --demo
```

For desktop editing, first launch:

```sh
filmcraft --control 9876
```

Then configure the MCP client to launch:

```sh
filmcraft-cli mcp --bridge 127.0.0.1:9876
```

Use one server mode for the intended project. A headless session and the desktop app are separate sessions. Keep the desktop control interface on loopback. The headless server has the filesystem permissions of its process; upstream does not provide folder-confinement flags.

After connecting, verify that `command_list` and `doc_inspect` return valid results for the intended session before editing.

Full upstream agent documentation:
https://github.com/storytold/filmcraft/blob/8309f21a6c3f34ddf190af7fd9bfd913053a1fd5/docs/agents.md
