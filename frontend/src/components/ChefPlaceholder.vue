<template>
  <div class="chef-placeholder" aria-hidden="true">
    <svg viewBox="0 0 64 64" class="chef-icon" role="img" focusable="false">
      <ellipse cx="32" cy="15" rx="13" ry="8" fill="#ffffff" />
      <rect x="19" y="15" width="26" height="10" fill="#ffffff" />
      <ellipse cx="32" cy="25" rx="13" ry="4" fill="#ececec" />
      <circle cx="32" cy="34" r="10" fill="#f3cda3" />
      <path d="M23 33c0-5 4-9 9-9s9 4 9 9" fill="#3c2a1d" />
      <circle cx="28" cy="34" r="1.3" fill="#1b1b1b" />
      <circle cx="36" cy="34" r="1.3" fill="#1b1b1b" />
      <path d="M28 39c1.2 1.3 2.6 2 4 2s2.8-.7 4-2" stroke="#8f5f42" stroke-width="1.6" fill="none" stroke-linecap="round" />
      <path d="M18 60c1-8 6-14 14-14s13 6 14 14" fill="#ffffff" />
    </svg>
  </div>
</template>

<style scoped>
.chef-placeholder {
  width: 100%;
  height: 100%;
  border-radius: inherit;
  clip-path: circle(50% at 50% 50%);
  display: grid;
  place-items: center;
  background: linear-gradient(180deg, #f0e2cf 0%, #e5d1b8 100%);
}

.chef-icon {
  width: 78%;
  height: 78%;
  border-radius: 50%;
}
</style>
