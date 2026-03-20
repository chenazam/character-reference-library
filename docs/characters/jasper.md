# Jasper

<div class="character-header">

--8<-- "snippets/galleries/jasper/hero.md"

<div class="character-overview-text">

<p>Jasper is a compact, runner-built man with a lean athletic physique and a strong lower-body emphasis. His narrow waist, powerful thighs, and prominent rounded glutes create a leg-dominant silhouette that reads agile, energetic, and physically expressive.</p>

<p>His style combines playful athletic fashion with a more revealing, attention-seeking edge, especially through very short-inseam athletic shorts and fitted sporty clothing. He comes across as warm, flirtatious, and socially confident, with an easy charm that makes his presence feel lively and inviting.</p>

<p>---</p>

<div class="character-stats">
<ul>
  <li><strong>Height:</strong> 170 cm / 5&#x27;7&quot;</li>
  <li><strong>Build:</strong> runner build</li>
  <li><strong>Silhouette:</strong> leg dominant</li>
  <li><strong>Face:</strong> oval and defined jawline</li>
  <li><strong>Hair:</strong> short light brown / dark blonde hair with soft natural texture</li>
  <li><strong>Eyes:</strong> expressive eyes with lively warmth</li>
  <li><strong>Style:</strong> exhibitionist, athletic, and streetwear</li>
  <li><strong>Palette:</strong> pink, soft red, light grey, and navy</li>
  <li><strong>Materials:</strong> cotton and mesh</li>
  <li><strong>Expression:</strong> soft neutral and open warm</li>
  <li><strong>Movement:</strong> restless quick</li>
  <li><strong>Presence:</strong> energetic</li>
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
      <img class="height-lineup__silhouette height-lineup__silhouette--reference" src="/assets/reference/reference_male_average_180cm_front_v1.png" alt="Reference silhouette" style="height: 100.00%;">
    </div>
    <div class="height-lineup__label">Reference</div>
    <div class="height-lineup__meta">180 cm / 5'11"</div>
  </div>

  <div class="height-lineup__figure height-lineup__figure--a">
    <div class="height-lineup__stage">
      <img class="height-lineup__silhouette" src="/assets/library/10_CHARACTERS/JASPER/02_BODY/structure/jasper_silhouette_front_v1_normalized.png" alt="Jasper silhouette front" style="height: 94.44%;">
    </div>
    <div class="height-lineup__label">Jasper</div>
    <div class="height-lineup__meta">170 cm / 5'7"</div>
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

--8<-- "snippets/galleries/jasper/identity.md"

---

## Body

--8<-- "snippets/galleries/jasper/body.md"

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
