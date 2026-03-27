# Hudson

<div class="character-header">

--8<-- "snippets/galleries/hudson/hero.md"

<div class="character-overview-text">

<p>Hudson is a tall, broad-shouldered athletic man with a muscular build and a controlled, dominant presence. His narrow angular facial structure and short brown hair give him a clean, disciplined look, while his body proportions emphasize strength, balance, and physical composure.</p>

<p>His aesthetic blends athletic luxury with minimalist sport-influenced styling, creating a polished image that feels deliberate and restrained. He projects calm authority and self-control, with a physical presence that is confident without needing overt display.</p>

<p>---</p>

<div class="character-stats">
<ul>
  <li><strong>Height:</strong> 188 cm / 6&#x27;2</li>
  <li><strong>Build:</strong> athletic muscular</li>
  <li><strong>Silhouette:</strong> balanced frame</li>
  <li><strong>Face:</strong> narrow angular and defined jawline</li>
  <li><strong>Hair:</strong> short brown hair with natural texture and slightly tousled volume</li>
  <li><strong>Eyes:</strong> light blue-green eyes with focused, confident gaze</li>
  <li><strong>Style:</strong> athletic luxury and athletic</li>
  <li><strong>Palette:</strong> black and white</li>
  <li><strong>Materials:</strong> cotton</li>
  <li><strong>Expression:</strong> confident neutral and controlled</li>
  <li><strong>Movement:</strong> relaxed natural</li>
  <li><strong>Presence:</strong> expansive presence</li>
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
      <img class="height-lineup__silhouette height-lineup__silhouette--reference" src="/assets/reference/reference_male_average_180cm_front_v1.png" alt="Reference silhouette" style="height: 95.74%;">
    </div>
    <div class="height-lineup__label">Reference</div>
    <div class="height-lineup__meta">180 cm / 5'11"</div>
  </div>

  <div class="height-lineup__figure height-lineup__figure--a">
    <div class="height-lineup__stage">
      <img class="height-lineup__silhouette" src="/assets/library/10_CHARACTERS/HUDSON/02_BODY/structure/hudson_silhouette_front_v1_normalized.png" alt="Hudson silhouette front" style="height: 100.00%;">
    </div>
    <div class="height-lineup__label">Hudson</div>
    <div class="height-lineup__meta">188 cm / 6'2</div>
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

--8<-- "snippets/galleries/hudson/identity.md"

---

## Body

--8<-- "snippets/galleries/hudson/body.md"

---

## Style

--8<-- "snippets/galleries/hudson/style.md"

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
