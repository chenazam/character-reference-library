# Lucien

<div class="character-header">

--8<-- "snippets/galleries/lucien/hero.md"

<div class="character-overview-text">

<p>Lucien is a slender, narrow-framed man with refined features, expressive dark eyes, and naturally curly dark hair. His physique is lightly built with a slim torso and narrow shoulders, while the lower body carries slightly more volume in the hips and glutes, creating a subtle leg-dominant silhouette that contrasts with his otherwise delicate frame.</p>

<p>His overall aesthetic blends occult symbolism with scholarly elegance and restrained gothic styling. Dark layered clothing, antique jewelry, and talismanic accessories give him the appearance of a modern practitioner of arcane traditions rather than a theatrical fantasy mage. Lucien’s presence is calm and observant, with a quiet confidence and a hint of playful mischief that suggests he knows more than he immediately reveals.</p>

<p>---</p>

<div class="character-stats">
<ul>
  <li><strong>Height:</strong> 170 cm / 5&#x27;7&quot;</li>
  <li><strong>Build:</strong> narrow slender</li>
  <li><strong>Silhouette:</strong> leg dominant</li>
  <li><strong>Face:</strong> narrow angular and defined jawline</li>
  <li><strong>Hair:</strong> dark brown naturally curly hair with soft volume and an irregular natural hairline</li>
  <li><strong>Eyes:</strong> dark brown, observant and expressive</li>
  <li><strong>Style:</strong> occult, scholarly, and gothic</li>
  <li><strong>Palette:</strong> black and charcoal</li>
  <li><strong>Materials:</strong> wool, velvet, and antique metal</li>
  <li><strong>Expression:</strong> calm reserved and controlled</li>
  <li><strong>Movement:</strong> deliberate precise</li>
  <li><strong>Presence:</strong> neutral presence</li>
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
      <img class="height-lineup__silhouette" src="/assets/library/10_CHARACTERS/LUCIEN/02_BODY/structure/lucien_silhouette_front_v1_normalized.png" alt="Lucien silhouette front" style="height: 94.44%;">
    </div>
    <div class="height-lineup__label">Lucien</div>
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

--8<-- "snippets/galleries/lucien/identity.md"

---

## Body

--8<-- "snippets/galleries/lucien/body.md"

---

## Style

--8<-- "snippets/galleries/lucien/style.md"

---

## Motion

--8<-- "snippets/galleries/lucien/motion.md"

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
