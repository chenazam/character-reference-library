.height-lineup {
  --lineup-tick-column: 90px;
  --lineup-stage-height: 460px;
  --lineup-footer-height: 3.2rem;

  display: grid;
  grid-template-columns: var(--lineup-tick-column) repeat(3, minmax(0, 1fr));
  gap: 2rem;
  align-items: end;
  margin: 1rem 0 2rem;
  position: relative;
}

.height-lineup--multi {
  grid-template-columns: var(--lineup-tick-column) repeat(auto-fit, minmax(140px, 1fr));
}

.height-lineup__ticks {
  position: absolute;
  left: 0;
  width: var(--lineup-tick-column);
  height: var(--lineup-stage-height);
  bottom: var(--lineup-footer-height);
  z-index: 0;
}

.height-lineup__tick {
  position: absolute;
  left: 0;
  right: 0;
  border-top: 1px solid var(--md-default-fg-color--lighter);
}

.height-lineup__tick-label {
  position: absolute;
  top: -0.7rem;
  left: 0;
  font-size: 0.72rem;
  color: var(--md-default-fg-color--light);
  background: var(--md-default-bg-color);
  padding-right: 0.35rem;
}

.height-lineup__baseline {
  position: absolute;
  left: var(--lineup-tick-column);
  right: 0;
  bottom: var(--lineup-footer-height);
  height: 2px;
  background: var(--md-default-fg-color);
  z-index: 0;
}

.height-lineup__figure {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
}

.height-lineup__figure--ref {
  grid-column: 2;
}

.height-lineup__figure--a {
  grid-column: 3;
}

.height-lineup__figure--b {
  grid-column: 4;
}

.height-lineup__stage {
  width: 100%;
  max-width: 260px;
  height: var(--lineup-stage-height);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding: 0 1rem;
  position: relative;
}

.height-lineup__label {
  margin-top: 0.75rem;
  font-size: 0.95rem;
  font-weight: 600;
  text-align: center;
}

.height-lineup__meta {
  font-size: 0.8rem;
  color: var(--md-default-fg-color--light);
  text-align: center;
}

.height-lineup__silhouette {
  max-width: 100%;
  width: auto;
  object-fit: contain;
  object-position: bottom center;
  display: block;
}

.height-lineup__placeholder {
  max-width: 100%;
  opacity: 0.55;
  background: var(--md-default-fg-color--light);
  display: block;
  margin: 0 auto;
}

.height-lineup__placeholder--reference {
  opacity: 0.3;
}

.height-lineup__placeholder--slender {
  width: 84px;
  clip-path: polygon(
    42% 0%, 58% 0%, 64% 8%, 64% 20%, 73% 37%, 68% 100%,
    56% 100%, 53% 60%, 47% 60%, 44% 100%, 32% 100%, 27% 37%,
    36% 20%, 36% 8%
  );
}

.height-lineup__placeholder--athletic {
  width: 104px;
  clip-path: polygon(
    40% 0%, 60% 0%, 67% 8%, 67% 20%, 80% 37%, 73% 100%,
    57% 100%, 54% 62%, 46% 62%, 43% 100%, 27% 100%, 20% 37%,
    33% 20%, 33% 8%
  );
}

.height-lineup__placeholder--broad {
  width: 124px;
  clip-path: polygon(
    39% 0%, 61% 0%, 69% 8%, 69% 20%, 85% 38%, 76% 100%,
    58% 100%, 55% 64%, 45% 64%, 42% 100%, 24% 100%, 15% 38%,
    31% 20%, 31% 8%
  );
}

.height-lineup__placeholder--massive {
  width: 144px;
  clip-path: polygon(
    38% 0%, 62% 0%, 70% 8%, 70% 20%, 88% 39%, 79% 100%,
    59% 100%, 56% 66%, 44% 66%, 41% 100%, 21% 100%, 12% 39%,
    30% 20%, 30% 8%
  );
}

@media (max-width: 1050px) {
  .height-lineup {
    grid-template-columns: 1fr;
  }

  .height-lineup__ticks,
  .height-lineup__baseline {
    display: none;
  }

  .height-lineup__figure--ref,
  .height-lineup__figure--a,
  .height-lineup__figure--b {
    grid-column: auto;
  }
}
