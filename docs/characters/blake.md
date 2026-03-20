# Blake

<div class="character-header">

--8<-- "snippets/galleries/blake/hero.md"

<div class="character-overview-text">

<p>Blake is a tall, muscular athlete with a calm, grounded presence and a powerful upper-body-dominant silhouette. His broad shoulders, strong chest, and thick arms give him a physically imposing frame, but his overall read is steady and protective rather than aggressive.</p>

<p>His style blends polished athletic clothing with understated luxury influences, creating a look that feels modern, masculine, and quietly confident. He projects stability, self-assurance, and relaxed physical strength in both posture and expression.</p>

<p>---</p>

<div class="character-stats">
<ul>
  <li><strong>Height:</strong> 191 cm / 6&#x27;3&quot;</li>
  <li><strong>Build:</strong> athletic muscular</li>
  <li><strong>Silhouette:</strong> upper body dominant</li>
  <li><strong>Face:</strong> square and defined jawline</li>
  <li><strong>Hair:</strong> short dark brown hair with clean athletic styling</li>
  <li><strong>Eyes:</strong> calm confident eyes</li>
  <li><strong>Style:</strong> athletic luxury, luxury, and streetwear</li>
  <li><strong>Palette:</strong> black, charcoal, and dark navy</li>
  <li><strong>Materials:</strong> cotton, mesh, and wool</li>
  <li><strong>Expression:</strong> confident neutral and controlled</li>
  <li><strong>Movement:</strong> grounded powerful</li>
  <li><strong>Presence:</strong> dominant presence</li>
</ul>
</div>

</div>

</div>

---

## Height Context

<div class="height-lineup height-lineup--character-context">
  <div class="height-lineup__baseline" aria-hidden="true"></div>

  <div class="height-lineup__figure height-lineup__figure--ref">
    <div class="height-lineup__stage">
      <img class="height-lineup__silhouette height-lineup__silhouette--reference" src="/assets/reference/reference_male_average_180cm_front_v1.png" alt="Reference silhouette" style="height: 94.24%;">
    </div>
    <div class="height-lineup__label">Reference</div>
    <div class="height-lineup__meta">180 cm / 5'11"</div>
  </div>

  <div class="height-lineup__figure height-lineup__figure--a">
    <div class="height-lineup__stage">
      <img class="height-lineup__silhouette" src="/assets/library/10_CHARACTERS/BLAKE/02_BODY/structure/blake_silhouette_front_v1.png" alt="Blake silhouette front" style="height: 100.00%;">
    </div>
    <div class="height-lineup__label">Blake</div>
    <div class="height-lineup__meta">191 cm / 6'3"</div>
  </div>
</div>



---

<div class="gallery-version-toggle" role="group" aria-label="Asset version display">
  <label class="gallery-version-toggle__label">
    <input class="gallery-version-toggle__input" type="checkbox" id="show-all-versions-toggle">
    <span>Show all versions</span>
  </label>
</div>

## Identity

--8<-- "snippets/galleries/blake/identity.md"

---

## Body

--8<-- "snippets/galleries/blake/body.md"

---

## Scenes

--8<-- "snippets/galleries/blake/scenes.md"

---

<script>
document.addEventListener('DOMContentLoaded', function () {
  var toggle = document.getElementById('show-all-versions-toggle');
  if (!toggle) return;
  var root = document.documentElement;
  var storageKey = 'character-gallery-version-mode';
  try {
    if (window.localStorage && localStorage.getItem(storageKey) === 'all') {
      toggle.checked = true;
    }
  } catch (error) {}

  function applyMode() {
    var mode = toggle.checked ? 'all' : 'latest';
    root.setAttribute('data-gallery-versions', mode);
    try {
      if (window.localStorage) {
        localStorage.setItem(storageKey, mode);
      }
    } catch (error) {}
  }

  toggle.addEventListener('change', applyMode);
  applyMode();
});
</script>
