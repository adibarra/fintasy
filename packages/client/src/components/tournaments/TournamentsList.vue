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

const tournaments = ref<Tournament[]>([])
const tournamentDetails = ref<Tournament>()
const showModal = ref(false)
const currentPage = ref(0)
const totalPages = ref(1)

async function fetchTournaments(page: number) {
  const params = {
    owner: props.filters.owner,
    name: props.filters.name,
    status: props.filters.status,
    start_date: props.filters.dateTimeRange?.[0]?.toISOString() ?? undefined,
    end_date: props.filters.dateTimeRange?.[1]?.toISOString() ?? undefined,
    offset: (page - 1) * 10,
    limit: 11,
  }

  const response = await fintasy.getTournaments(params)
  if (response.code === 200)
    tournaments.value = response.data
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

function joinTournament(uuid: string) {
  console.log(`Joining tournament ${uuid}`)
  // need logic for joining a tournament
  closeTournamentModal()
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
      :disabled="currentPage <= 1"
      @click="changePage(currentPage - 1)"
    >
      Prev
    </button>
    <button
      :disabled="currentPage >= totalPages"
      @click="changePage(currentPage + 1)"
    >
      Next
    </button>
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
