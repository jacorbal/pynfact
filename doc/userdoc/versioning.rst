.. vim: set ft=rst fenc=utf-8 tw=72 nowrap:

**********
Versioning
**********

This project uses the `Semantic Versioning Specification 2.0.0`_,
(*X.Y.Z*) where:

* *X* is the *major* version;
* *Y* is the *minor* version; and
* *Z* is the *patch* version, or *micro* version.

The version increment goes as:

* *X* or *major*, when there are incompatible API changes;
* *Y* or *minor* version new functionality is added in a backwards
  compatible manner; and
* *Z* or *patch* version when there are backwards compatible bug
  fixes.

In the case of pre-releases, it's appended a suffix, that for
compatibility with Python version control, it's separated by a dot when
needed.  Examples of this versions are:

* ``2.0.1.devN``: Developing version *N*
* ``2.0.1aN``: Alpha version *N*
* ``2.0.1bN``: Beta version *N*
* ``2.0.1rcN``: Release candidate *N*
* ``2.0.1``: Stable release
* ``2.0.1.postN``: Post release version *N*

More information: `Semantic Versioning 2.0.0`__.


.. _`Semantic Versioning Specification 2.0.0`: https://semver.org/
__ `Semantic Versioning Specification 2.0.0`_
