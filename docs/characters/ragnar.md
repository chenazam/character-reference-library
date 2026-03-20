# Ragnar

<div class="character-header">

--8<-- "snippets/galleries/ragnar/hero.md"

<div class="character-overview-text">

<p>Ragnar is an extremely tall warrior whose presence is defined by overwhelming physical scale and dense muscular mass. His frame is broad and heavily shoulder-dominant, with a thick chest, powerful arms, and a solid, grounded stance that makes him appear immovable. Even at rest, his posture carries the calm weight of someone used to physical dominance and battlefield control.</p>

<p>His face is square and strongly structured, with a sharp jawline, calm blue eyes, and a short blond beard that reinforces his rugged masculinity. Long blond hair falls to his shoulders in natural waves, framing a composed and watchful expression. Ragnar’s overall visual identity blends towering warrior strength with stoic restraint, creating a silhouette that reads as massive, controlled, and quietly intimidating.</p>

<p>---</p>

<div class="character-stats">
<ul>
  <li><strong>Height:</strong> 208 cm / 6&#x27;10&quot;</li>
  <li><strong>Build:</strong> heavy muscular</li>
  <li><strong>Silhouette:</strong> shoulder dominant</li>
  <li><strong>Face:</strong> square and sharp jawline</li>
  <li><strong>Hair:</strong> long blond hair with natural volume, often worn loose</li>
  <li><strong>Eyes:</strong> calm blue eyes with steady, watchful focu</li>
  <li><strong>Style:</strong> rugged utilitarian, military, and gothic</li>
  <li><strong>Palette:</strong> black and dark brown</li>
  <li><strong>Materials:</strong> leather and antique metal</li>
  <li><strong>Expression:</strong> serious controlled and controlled</li>
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
      <img class="height-lineup__silhouette height-lineup__silhouette--reference" src="/assets/reference/reference_male_average_180cm_front_v1.png" alt="Reference silhouette" style="height: 86.54%;">
    </div>
    <div class="height-lineup__label">Reference</div>
    <div class="height-lineup__meta">180 cm / 5'11"</div>
  </div>

  <div class="height-lineup__figure height-lineup__figure--a">
    <div class="height-lineup__stage">
      <img class="height-lineup__silhouette" src="/assets/library/10_CHARACTERS/RAGNAR/02_BODY/structure/ragnar_silhouette_front_v1_normalized.png" alt="Ragnar silhouette front" style="height: 100.00%;">
    </div>
    <div class="height-lineup__label">Ragnar</div>
    <div class="height-lineup__meta">208 cm / 6'10"</div>
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

--8<-- "snippets/galleries/ragnar/identity.md"

---

## Body

--8<-- "snippets/galleries/ragnar/body.md"

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
