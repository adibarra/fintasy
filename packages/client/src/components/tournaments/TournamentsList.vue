<!--
  @author: adibarra (Alec Ibarra), Zedfoura (Tinatsei Chingaya)
  @description: This component is used to display the list of tournaments on the tournaments page of the application.
-->

<script setup lang="ts">
import { useMessage } from 'naive-ui'
import type { STATUS, Tournament } from '~/types'

interface TournamentFilter {
  owner?: string
  name?: string
  status?: STATUS
  start_date?: Date
  end_date?: Date
}

const props = defineProps({
  filters: {
    type: Object as PropType<TournamentFilter>,
    required: true,
  },
})

const fintasy = useAPI()
const state = useStateStore()
const router = useRouter()
const message = useMessage()

const tournamentDetails = ref<Tournament>()
const showModal = ref(false)
const currentPage = ref(1)
const itemsPerPage = ref(10)

const filteredTournaments = computed(() => {
  return state.tournaments.filter((tournament) => {
    const filters = props.filters
    const meetsOwner = !filters.owner || tournament.owner.includes(filters.owner)
    const meetsName = !filters.name || tournament.name.toLowerCase().includes(filters.name.toLowerCase())
    const meetsStatus = !filters.status || tournament.status === filters.status
    const meetsStartDate = !filters.start_date || new Date(tournament.start_date) >= new Date(filters.start_date)
    const meetsEndDate = !filters.end_date || new Date(tournament.end_date) <= new Date(filters.end_date)

    return meetsOwner && meetsName && meetsStatus && meetsStartDate && meetsEndDate
  })
})

const numFilteredTournaments = computed(() => filteredTournaments.value.length)
const totalPages = computed(() => Math.ceil(numFilteredTournaments.value / itemsPerPage.value))
const displayedTournaments = computed(() => {
  return filteredTournaments.value.slice((currentPage.value - 1) * itemsPerPage.value, currentPage.value * itemsPerPage.value)
})

async function viewTournament(uuid: string) {
  const response = await fintasy.getTournament({ uuid })
  if (response.code !== 200) {
    console.error('Failed to load tournament details.')
    return
  }

  tournamentDetails.value = response.data
  showModal.value = true
}

async function joinTournament(uuid: string) {
  const tournamentResponse = await fintasy.getTournament({ uuid })
  if (tournamentResponse.code !== 200) {
    console.error('Failed to fetch tournament details')
    return
  }

  // Proceed to create a portfolio
  const portfolioResponse = await fintasy.createPortfolio({ name: tournamentResponse.data.name, tournament: uuid })
  if (portfolioResponse.code !== 200) {
    console.error('Failed to create portfolio:', portfolioResponse)
    return
  }

  message.success('Portfolio created successfully')
  await state.refresh.portfolios()
  state.portfolio.active = state.portfolio.available.findIndex(p => p.uuid === portfolioResponse.data.uuid)
  router.push('/dashboard/trade')
  closeTournamentModal()
}

function closeTournamentModal() {
  showModal.value = false
}

function nextPage() {
  if (currentPage.value < totalPages.value)
    currentPage.value++
}

function prevPage() {
  if (currentPage.value > 1)
    currentPage.value--
}

watch([itemsPerPage, () => props.filters], () => {
  currentPage.value = 1 // Resets to first page when any filter changes
}, { deep: true })
</script>

<template>
  <div class="tournaments-list">
    <div
      v-for="(tournament, index) in displayedTournaments"
      :key="index"
      class="tournament-card"
    >
      <div flex justify-between>
        <div>
          <h3>{{ tournament.name }}</h3>
          <p>{{ tournament.status }}</p>
        </div>
        <div flex gap-2>
          <button fn-outline px-2 py-1 fn-hover @click="viewTournament(tournament.uuid)">
            View
          </button>
          <button fn-outline px-2 py-1 fn-hover @click="joinTournament(tournament.uuid)">
            Join Tournament
          </button>
        </div>
      </div>
    </div>
    <div>
      <div class="pagination-container">
        <button
          fn-outline px-2 py-1 fn-hover
          :disabled="currentPage <= 1"
          :class="{ 'op-50': currentPage <= 1 }"
          @click="prevPage"
        >
          &lt; Prev
        </button>
        <span class="page-indicator">Page {{ currentPage }} of {{ totalPages }}</span>
        <button
          fn-outline px-2 py-1 fn-hover
          :disabled="currentPage >= totalPages"
          :class="{ 'op-50': currentPage >= totalPages }"
          @click="nextPage"
        >
          Next &gt;
        </button>
      </div>
      <div flex justify-right>
        <select v-model="itemsPerPage" class="items-per-page-selector">
          <option :value="5">
            5
          </option>
          <option default :value="10">
            10
          </option>
          <option :value="20">
            20
          </option>
          <option :value="40">
            40
          </option>
          <option :value="60">
            60
          </option>
        </select>
      </div>
    </div>
    <TournamentModal v-if="tournamentDetails" :visible="showModal" :tournament="tournamentDetails" @close="closeTournamentModal" />
  </div>
</template>

<style scoped>
.pagination-container {
  display: flex;
  align-items: center; /* Ensures vertical centering */
  justify-content: center; /* Centers the pagination horizontally */
  gap: 10px; /* Adds space between elements */
}

.tournaments-list {
  display: flex;
  flex-direction: column;
}

.tournament-card {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}

.items-per-page-selector {
  padding: 5px 10px; /* Adjust padding as needed for visual consistency */
  background: rgb(22, 22, 22); /* Optional: changes background color */
  border: 1px solid #ccc; /* Optional: adds border */
}

.page-indicator {
  min-width: 120px; /* Ensures the page indicator has sufficient width */
  text-align: center; /* Centers the text inside the span */
}
</style>
