# Coding Best Practices

Provider-neutral agent skills for writing, reviewing, and maintaining code and infrastructure.

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <img src="images/logo.png" alt="Logo" width="80" height="80">

  <p align="center">
    <a href="https://github.com/JSChronicles/coding-best-practices"><strong>Explore the docs »</strong></a>
    <br />
    <a href="https://github.com/JSChronicles/coding-best-practices/issues/new?labels=Bug%2CNeeds+Triage&projects=&template=bug.yaml&title=%5BBUG%5D+%3Ctitle%3E">Report Bug</a>
    ·
    <a href="https://github.com/JSChronicles/coding-best-practices/issues/new?labels=enhancement%2Cfeature+request&projects=&template=feature.yaml&title=%5BFEATURE%5D%3A+">Request Feature</a>
  </p>
</div>

## Included skills

- `python-best-practices`
- `powershell-best-practices`
- `terraform-best-practices`

Each skill is maintained once under `skills/`. Product-specific manifests expose those same canonical skill directories rather than maintaining copies.

## Codex CLI and ChatGPT desktop app

Add the GitHub repository as a marketplace:

```text
codex plugin marketplace add JSChronicles/coding-best-practices --ref main
```

Open `/plugins`, select the **Coding Best Practices** marketplace, and install the plugin. Start a new chat after installation or an upgrade.

Refresh configured marketplaces with:

```text
codex plugin marketplace upgrade
```

## Claude Code

Add the repository as a marketplace and install the plugin:

```text
/plugin marketplace add JSChronicles/coding-best-practices
/plugin install coding-best-practices@coding-best-practices
```

Start a new Claude Code session after installation or an upgrade.

## Other agents

Agents that support the Agent Skills layout can install individual directories from `skills/` at user or project scope. Installation locations and update mechanisms vary by agent. The skill content avoids provider-specific terminology so the same package can be adapted without changing its instructions.

## Contributing

Keep each skill focused and provider-neutral. Put detailed, conditional guidance in `references/`, link it from `SKILL.md`, and validate changed skills before publishing a new package version.
