# article-audit

## Purpose

Audit whether one article slug has a complete and consistent artifact family.

## Use Cases

- checking publish readiness for one article
- verifying that brief, draft, cover, and inline images align under one slug
- finding missing or misnamed article artifacts

## Trigger Examples

- `检查这篇文章是否齐全`
- `审计这篇文章`
- `article audit`
- `publish ready`

## Inputs

- article slug
- optional article path

## Outputs

- artifact presence report
- naming consistency report
- readiness level

## Boundary

This skill audits one article family. It does not replace repository-wide cleanup handled by `package-neat`.

One of its key checks is whether later artifacts drifted away from the original slug.
