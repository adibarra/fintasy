<script setup lang="ts">
import type { STATUS, Tournament } from '~/types'

const props = defineProps({
  filters: {
    type: Object as PropType<{
      owner: string | undefined
      name: string | undefined
      status: STATUS | undefined
      dateTimeRange: [Date, Date] | undefined
    }>,
    required: true,
  },
})

const fintasy = useAPI()
const state = useStateStore()

const tournaments = ref<Tournament[]>([])
const tournamentDetails = ref<Tournament>()
const showModal = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)

async function fetchTournaments(page: number) {
  const params = {
    owner: props.filters.owner,
    name: props.filters.name,
    status: props.filters.status,
    start_date: props.filters.dateTimeRange?.[0]?.toISOString() ?? undefined,
    end_date: props.filters.dateTimeRange?.[1]?.toISOString() ?? undefined,
    offset: (page - 1) * 10,
    limit: 10,
  }

  const response = await fintasy.getTournaments(params)
  if (response.code === 200) {
    tournaments.value = response.data
    totalPages.value = Math.ceil(response.data.length / 10)
    console.log(`Viewing tournament ${totalPages.value}`)
  }
}

async function viewTournament(uuid: string) {
  console.log(`Viewing tournament ${uuid}`)
  const response = await fintasy.getTournament({ uuid })
  if (response.code === 200) {
    tournamentDetails.value = response.data
    showModal.value = true
  }
  else {
    alert('Failed to load tournament details.') // Or handle this error differently
  }
}

async function joinTournament(uuid: string) {
  console.log(`Joining tournament ${uuid}`)
  let tournamentName = '' // Initialize a variable for the tournament name
  try {
    const tournamentResponse = await fintasy.getTournament({ uuid })
    if (tournamentResponse.code === 200)
      tournamentName = tournamentResponse.data.name
    else
      throw new Error('Failed to fetch tournament details')
  }
  catch (error) {
    console.error('Error fetching tournament details:', error)
    alert('Failed to load tournament details.') // Or handle this error differently
    return // Stop further execution if the tournament details cannot be fetched
  }

  // Construct the portfolio name based on the tournament name
  const portfolioName = `${tournamentName}`

  // Proceed to create a portfolio
  try {
    const portfolioResponse = await fintasy.createPortfolio({ name: portfolioName, tournament: uuid })
    console.log('Portfolio created successfully:', portfolioName, portfolioResponse)
    closeTournamentModal()
    const portfoliosRequest = await fintasy.getPortfolios({ owner: state.user.uuid, limit: 10 })
    if (portfoliosRequest.code !== 200)
      return

    state.portfolio.active = 0
    state.portfolio.available = portfoliosRequest.data

    if (portfoliosRequest.data.length !== 0)
      return

    const createPortfolioRequest = await fintasy.createPortfolio({ name: 'Default Portfolio' })
    if (createPortfolioRequest.code !== 200)
      return

    state.portfolio.available = [createPortfolioRequest.data]
  }
  catch (error) {
    console.error('Failed to create portfolio:', error)
    // You might want to handle this error in the UI, e.g., showing an error message to the user
  }
}

function closeTournamentModal() {
  showModal.value = false
}

function changePage(page: number) {
  if (page < 1 || page > totalPages.value)
    return
  currentPage.value = page
  fetchTournaments(page)
}

watch(() => props.filters, () => {
  fetchTournaments(currentPage.value)
}, { deep: true, immediate: true })
</script>

<template>
  <div class="tournaments-list">
    <div
      v-for="(tournament, index) in tournaments"
      :key="index"
      class="tournament-card"
    >
      <h3>{{ tournament.name }}</h3>
      <p>{{ tournament.status }}</p>
      <button
        @click="viewTournament(tournament.uuid)"
      >
        View
      </button>
      <button
        @click="joinTournament(tournament.uuid)"
      >
        Quick Join
      </button>
    </div>
    <button
      :disabled="currentPage.data <= 1"
      @click="changePage(currentPage.data - 1)"
    >
      Prev
    </button>
    <button
      :disabled="currentPage.data >= totalPages.data"
      @click="changePage(currentPage.data + 1)"
    >
      Next
    </button>
    <TournamentModal :visible="showModal" :tournament="tournamentDetails" @close="closeTournamentModal" />
  </div>
</template>

<style scoped>
.tournaments-list {
  display: flex;
  flex-direction: column;
}
.tournament-card {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}
</style>
