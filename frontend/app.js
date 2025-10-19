const API_BASE_URL = import.meta?.env?.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

const DEFAULT_FILTERS = Object.freeze({
  search: "",
  category: "",
  minBid: "",
  maxBid: "",
  endingAfter: "",
  endingBefore: "",
});

const DEFAULT_EMPTY_MESSAGE = "No listings found. Adjust your filters or try again later.";

const state = {
  listings: [],
  filtered: [],
  filters: { ...DEFAULT_FILTERS },
  categoryOptions: [],
  usingFallback: false,
};

const elements = {
  search: document.getElementById("search"),
  category: document.getElementById("category"),
  minBid: document.getElementById("min-bid"),
  maxBid: document.getElementById("max-bid"),
  endingAfter: document.getElementById("ending-after"),
  endingBefore: document.getElementById("ending-before"),
  clearFilters: document.getElementById("clear-filters"),
  grid: document.getElementById("listings-grid"),
  emptyState: document.getElementById("empty-state"),
  template: document.getElementById("listing-card-template"),
};

let searchDebounceHandle;

function hasActiveFilters(filters) {
  return [
    filters.search.trim(),
    filters.category,
    filters.minBid.trim(),
    filters.maxBid.trim(),
    filters.endingAfter,
    filters.endingBefore,
  ].some(Boolean);
}

function parseNumberInput(value) {
  if (value === undefined || value === null || value === "") {
    return null;
  }
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function parseDateInput(value) {
  if (!value) {
    return null;
  }
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? null : parsed;
}

function buildQueryParams(filters) {
  const params = new URLSearchParams();
  const trimmedSearch = filters.search.trim();
  if (trimmedSearch) {
    params.set("search", trimmedSearch);
  }
  if (filters.category) {
    params.set("category", filters.category);
  }
  const minBid = parseNumberInput(filters.minBid);
  if (minBid !== null) {
    params.set("min_bid", String(minBid));
  }
  const maxBid = parseNumberInput(filters.maxBid);
  if (maxBid !== null) {
    params.set("max_bid", String(maxBid));
  }
  const endingAfterValue = filters.endingAfter?.trim();
  if (endingAfterValue) {
    params.set("ending_after", endingAfterValue);
  }
  const endingBeforeValue = filters.endingBefore?.trim();
  if (endingBeforeValue) {
    params.set("ending_before", endingBeforeValue);
  }
  return params;
}

async function fetchListings(filters) {
  const base = API_BASE_URL.endsWith("/") ? API_BASE_URL : `${API_BASE_URL}/`;
  const url = new URL("listings", base);
  const params = buildQueryParams(filters);
  params.forEach((value, key) => {
    url.searchParams.set(key, value);
  });

  const response = await fetch(url.toString());
  if (!response.ok) {
    throw new Error(`Failed to load listings (${response.status})`);
  }

  const data = await response.json();
  state.listings = data;
  state.filtered = data;
  state.usingFallback = false;

  const shouldResetCategories =
    state.categoryOptions.length === 0 || !hasActiveFilters(filters);
  populateCategories(data, { reset: shouldResetCategories });
  renderListings();
}

function ensureFallbackNotice() {
  if (document.querySelector(".fallback-notice")) {
    return;
  }
  const notice = document.createElement("p");
  notice.className = "fallback-notice";
  notice.textContent = "Showing sample data because the live API is offline.";
  document.querySelector("main")?.prepend(notice);
}

async function loadFallbackListings() {
  try {
    const response = await fetch("sample-data/listings.json");
    if (!response.ok) {
      throw new Error(`Fallback data unavailable (${response.status})`);
    }
    const data = await response.json();
    state.listings = data;
    state.usingFallback = true;
    state.categoryOptions = [];
    populateCategories(data, { reset: true });
    ensureFallbackNotice();
    applyLocalFilters();
  } catch (fallbackError) {
    console.error(fallbackError);
    state.filtered = [];
    state.usingFallback = true;
    elements.grid.innerHTML = "";
    elements.emptyState.textContent =
      "Unable to load listings. Ensure the API is running or provide fallback data.";
    elements.emptyState.classList.remove("hidden");
  }
}

function populateCategories(listings, { reset = false } = {}) {
  const categories = new Set(reset ? [] : state.categoryOptions);
  for (const item of listings) {
    if (item?.category) {
      categories.add(item.category);
    }
  }

  state.categoryOptions = Array.from(categories).sort((a, b) => a.localeCompare(b));
  const selectedCategory = state.filters.category;

  elements.category.innerHTML = "";
  const placeholder = document.createElement("option");
  placeholder.value = "";
  placeholder.textContent = "All categories";
  elements.category.append(placeholder);

  for (const category of state.categoryOptions) {
    const option = document.createElement("option");
    option.value = category;
    option.textContent = category;
    if (category === selectedCategory) {
      option.selected = true;
    }
    elements.category.append(option);
  }

  if (selectedCategory && !state.categoryOptions.includes(selectedCategory)) {
    state.filters.category = "";
    elements.category.value = "";
  }
}

function applyLocalFilters() {
  const normalizedSearch = state.filters.search.trim().toLowerCase();
  const category = state.filters.category;
  const minBid = parseNumberInput(state.filters.minBid);
  const maxBid = parseNumberInput(state.filters.maxBid);
  const endingAfter = parseDateInput(state.filters.endingAfter);
  const endingBefore = parseDateInput(state.filters.endingBefore);

  state.filtered = state.listings.filter((listing) => {
    const matchesSearch = normalizedSearch
      ? [listing.title, listing.description, listing.location]
          .filter(Boolean)
          .some((value) => value.toLowerCase().includes(normalizedSearch))
      : true;

    const matchesCategory = category ? listing.category === category : true;
    const matchesMinBid =
      minBid !== null ? Number(listing.current_bid) >= minBid : true;
    const matchesMaxBid =
      maxBid !== null ? Number(listing.current_bid) <= maxBid : true;

    const endTime = new Date(listing.end_time);
    if (Number.isNaN(endTime.getTime())) {
      return false;
    }
    const matchesEndingAfter = endingAfter ? endTime > endingAfter : true;
    const matchesEndingBefore = endingBefore ? endTime < endingBefore : true;

    return (
      matchesSearch &&
      matchesCategory &&
      matchesMinBid &&
      matchesMaxBid &&
      matchesEndingAfter &&
      matchesEndingBefore
    );
  });

  renderListings();
}

function renderListings() {
  elements.grid.innerHTML = "";
  elements.emptyState.textContent = DEFAULT_EMPTY_MESSAGE;

  if (state.filtered.length === 0) {
    elements.emptyState.classList.remove("hidden");
    return;
  }

  elements.emptyState.classList.add("hidden");

  for (const listing of state.filtered) {
    const card = elements.template.content.cloneNode(true);
    const thumbnail = card.querySelector(".listing-thumbnail");
    const title = card.querySelector(".listing-title");
    const bid = card.querySelector(".listing-bid");
    const end = card.querySelector(".listing-end");
    const location = card.querySelector(".listing-location");
    const description = card.querySelector(".listing-description");
    const link = card.querySelector(".listing-link");

    title.textContent = listing.title;
    bid.textContent = new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: listing.currency ?? "USD",
      maximumFractionDigits: 0,
    }).format(Number(listing.current_bid));

    const endTime = new Date(listing.end_time);
    end.textContent = endTime.toLocaleString(undefined, {
      dateStyle: "medium",
      timeStyle: "short",
    });

    location.textContent = listing.location;
    description.textContent = listing.description ?? "";

    if (listing.thumbnail_url) {
      thumbnail.src = listing.thumbnail_url;
      thumbnail.alt = `${listing.title} thumbnail`;
    } else {
      thumbnail.remove();
    }

    link.href = listing.url;

    elements.grid.append(card);
  }
}

function scheduleRefresh({ debounce = false } = {}) {
  if (debounce) {
    if (searchDebounceHandle) {
      clearTimeout(searchDebounceHandle);
    }
    searchDebounceHandle = setTimeout(() => {
      refreshListings();
    }, 250);
    return;
  }

  if (searchDebounceHandle) {
    clearTimeout(searchDebounceHandle);
  }
  refreshListings();
}

function attachEventListeners() {
  elements.search.addEventListener("input", (event) => {
    state.filters.search = event.target.value;
    scheduleRefresh({ debounce: true });
  });

  elements.category.addEventListener("change", (event) => {
    state.filters.category = event.target.value;
    scheduleRefresh();
  });

  elements.minBid.addEventListener("input", (event) => {
    state.filters.minBid = event.target.value;
    scheduleRefresh({ debounce: true });
  });

  elements.maxBid.addEventListener("input", (event) => {
    state.filters.maxBid = event.target.value;
    scheduleRefresh({ debounce: true });
  });

  elements.endingAfter.addEventListener("change", (event) => {
    state.filters.endingAfter = event.target.value;
    scheduleRefresh();
  });

  elements.endingBefore.addEventListener("change", (event) => {
    state.filters.endingBefore = event.target.value;
    scheduleRefresh();
  });

  elements.clearFilters.addEventListener("click", () => {
    Object.assign(state.filters, DEFAULT_FILTERS);
    elements.search.value = "";
    elements.category.value = "";
    elements.minBid.value = "";
    elements.maxBid.value = "";
    elements.endingAfter.value = "";
    elements.endingBefore.value = "";
    scheduleRefresh();
  });
}

async function refreshListings() {
  if (state.usingFallback) {
    applyLocalFilters();
    return;
  }

  try {
    await fetchListings(state.filters);
  } catch (error) {
    console.error(error);
    await loadFallbackListings();
  }
}

attachEventListeners();
refreshListings();
