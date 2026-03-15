# Asset Comparisons

Compare one asset type across all characters. Use the selector to switch between generated comparison grids.

<div class="comparison-controls">
  <label for="asset-type-select"><strong>Asset type:</strong></label>
  <select id="asset-type-select">
    <option value="gallery-image">01 Identity – Gallery Image</option>
    <option value="face-anchor">01 Identity – Face Anchor Sheet</option>
    <option value="face-front">01 Identity – Face Front</option>
    <option value="face-three-quarter">01 Identity – Face Three-Quarter</option>
    <option value="face-profile">01 Identity – Face Profile</option>
    <option value="hair-sheet">01 Identity – Hair Sheet</option>
    <option value="expression-sheet">01 Identity – Expression Sheet</option>
    <option value="hand-sheet">01 Identity – Hand Sheet</option>
    <option value="anatomy-sheet">02 Body – Anatomy Sheet</option>
    <option value="anatomy-front">02 Body – Anatomy Front</option>
    <option value="anatomy-side">02 Body – Anatomy Side</option>
    <option value="anatomy-back">02 Body – Anatomy Back</option>
    <option value="anatomy-glutes">02 Body – Glute Reference</option>
    <option value="body-anchor">02 Body – Body Anchor Sheet</option>
    <option value="proportion-grid">02 Body – Proportion Grid</option>
    <option value="muscle-tension">02 Body – Muscle Tension Sheet</option>
    <option value="silhouette-sheet">02 Body – Silhouette Sheet</option>
    <option value="turnaround-sheet">02 Body – Turnaround Sheet</option>
  </select>
</div>

<section class="comparison-section" data-asset-type="gallery-image">
<h2>01 Identity – Gallery Image</h2>

--8<-- "snippets/comparisons/gallery-image.md"

</section>

<section class="comparison-section" data-asset-type="face-anchor" hidden="hidden">
<h2>01 Identity – Face Anchor Sheet</h2>

--8<-- "snippets/comparisons/face-anchor.md"

</section>

<section class="comparison-section" data-asset-type="face-front" hidden="hidden">
<h2>01 Identity – Face Front</h2>

--8<-- "snippets/comparisons/face-front.md"

</section>

<section class="comparison-section" data-asset-type="face-three-quarter" hidden="hidden">
<h2>01 Identity – Face Three-Quarter</h2>

--8<-- "snippets/comparisons/face-three-quarter.md"

</section>

<section class="comparison-section" data-asset-type="face-profile" hidden="hidden">
<h2>01 Identity – Face Profile</h2>

--8<-- "snippets/comparisons/face-profile.md"

</section>

<section class="comparison-section" data-asset-type="hair-sheet" hidden="hidden">
<h2>01 Identity – Hair Sheet</h2>

--8<-- "snippets/comparisons/hair-sheet.md"

</section>

<section class="comparison-section" data-asset-type="expression-sheet" hidden="hidden">
<h2>01 Identity – Expression Sheet</h2>

--8<-- "snippets/comparisons/expression-sheet.md"

</section>

<section class="comparison-section" data-asset-type="hand-sheet" hidden="hidden">
<h2>01 Identity – Hand Sheet</h2>

--8<-- "snippets/comparisons/hand-sheet.md"

</section>

<section class="comparison-section" data-asset-type="anatomy-sheet" hidden="hidden">
<h2>02 Body – Anatomy Sheet</h2>

--8<-- "snippets/comparisons/anatomy-sheet.md"

</section>

<section class="comparison-section" data-asset-type="anatomy-front" hidden="hidden">
<h2>02 Body – Anatomy Front</h2>

--8<-- "snippets/comparisons/anatomy-front.md"

</section>

<section class="comparison-section" data-asset-type="anatomy-side" hidden="hidden">
<h2>02 Body – Anatomy Side</h2>

--8<-- "snippets/comparisons/anatomy-side.md"

</section>

<section class="comparison-section" data-asset-type="anatomy-back" hidden="hidden">
<h2>02 Body – Anatomy Back</h2>

--8<-- "snippets/comparisons/anatomy-back.md"

</section>

<section class="comparison-section" data-asset-type="anatomy-glutes" hidden="hidden">
<h2>02 Body – Glute Reference</h2>

--8<-- "snippets/comparisons/anatomy-glutes.md"

</section>

<section class="comparison-section" data-asset-type="body-anchor" hidden="hidden">
<h2>02 Body – Body Anchor Sheet</h2>

--8<-- "snippets/comparisons/body-anchor.md"

</section>

<section class="comparison-section" data-asset-type="proportion-grid" hidden="hidden">
<h2>02 Body – Proportion Grid</h2>

--8<-- "snippets/comparisons/proportion-grid.md"

</section>

<section class="comparison-section" data-asset-type="muscle-tension" hidden="hidden">
<h2>02 Body – Muscle Tension Sheet</h2>

--8<-- "snippets/comparisons/muscle-tension.md"

</section>

<section class="comparison-section" data-asset-type="silhouette-sheet" hidden="hidden">
<h2>02 Body – Silhouette Sheet</h2>

--8<-- "snippets/comparisons/silhouette-sheet.md"

</section>

<section class="comparison-section" data-asset-type="turnaround-sheet" hidden="hidden">
<h2>02 Body – Turnaround Sheet</h2>

--8<-- "snippets/comparisons/turnaround-sheet.md"

</section>

<script>
document.addEventListener('DOMContentLoaded', function () {
  const select = document.getElementById('asset-type-select');
  const sections = Array.from(document.querySelectorAll('.comparison-section'));

  function showAssetType(assetType) {
    sections.forEach((section) => {
      const isMatch = section.dataset.assetType === assetType;
      if (isMatch) {
        section.removeAttribute('hidden');
      } else {
        section.setAttribute('hidden', 'hidden');
      }
    });
  }

  if (select) {
    showAssetType(select.value);
    select.addEventListener('change', function () {
      showAssetType(select.value);
    });
  }
});
</script>
