# Security Policy

## Supported Versions

Security fixes are made against the latest published release. Please update to the latest version before reporting an issue. Older versions may not receive security fixes.

## Reporting a Vulnerability

Please report suspected vulnerabilities privately using
[GitHub's Report a vulnerability form](https://github.com/thienqo/flutter-skills/security/advisories/new).

Do not disclose vulnerability details in public issues, discussions, or pull requests.

If private reporting is unavailable, open an issue titled **“Security contact request”**
without including technical details. A maintainer will arrange a private channel.

Please include the affected version and distribution channel (npm, VS Code Marketplace,
Tessl, or GitHub), the potential impact, and steps to reproduce. Remove credentials,
tokens, and personal data from reports.

We will review reports and coordinate any fix and disclosure with the reporter.

## Scope

This repository distributes Agent Skills, an installer CLI, marketplace metadata, and
release workflows. Reports about vulnerabilities in these components or compromise of
the package and release process are in scope.

The skills provide guidance; they are not runtime security controls and do not guarantee
the security of Flutter applications built with them. Vulnerabilities in downstream
applications or their dependencies should be reported to those projects' maintainers.
