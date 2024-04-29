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

const tournaments = ref<Tournament[]>([])
const tournamentDetails = ref<Tournament>()
const showModal = ref(false)
const currentPage = ref(1)
const hasNextPage = ref(false)

async function fetchTournaments(page: number) {
  const params = {
    owner: props.filters.owner,
    name: props.filters.name,
    status: props.filters.status,
    start_date: props.filters.start_date?.toISOString() ?? undefined,
    end_date: props.filters.end_date?.toISOString() ?? undefined,
    offset: (page - 1) * 10,
    limit: 11,
  }

  const response = await fintasy.getTournaments(params)
  if (response.code !== 200) {
    console.error('Failed to fetch tournaments:', response)
    return
  }

  tournaments.value = response.data.slice(0, 10)
  hasNextPage.value = response.data.length === 11
}

async function viewTournament(uuid: string) {
  const response = await fintasy.getTournament({ uuid })
  if (response.code !== 200) {
    console.error('Failed to load tournament details.') // Or handle this error differently
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
  if (hasNextPage.value) {
    currentPage.value++
    fetchTournaments(currentPage.value)
  }
}

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--
    fetchTournaments(currentPage.value)
  }
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
      <div flex justify-between>
        <div>
          <h3>{{ tournament.name }}</h3>
          <p>{{ tournament.status }}</p>
        </div>
        <div flex gap-2>
          <button
            fn-outline px-2 py-1 fn-hover
            @click="viewTournament(tournament.uuid)"
          >
            View
          </button>
          <button
            fn-outline px-2 py-1 fn-hover
            @click="joinTournament(tournament.uuid)"
          >
            Quick Join
          </button>
        </div>
      </div>
    </div>
    <div flex justify-center gap-5>
      <button
        :disabled="currentPage <= 1"
        :class="{ 'op-50': currentPage <= 1 }"
        fn-outline px-2 py-1 fn-hover
        @click="prevPage"
      >
        &lt; Prev
      </button>
      <button
        :disabled="!hasNextPage"
        :class="{ 'op-50': !hasNextPage }"
        fn-outline px-2 py-1 fn-hover
        @click="nextPage"
      >
        Next
        &gt;
      </button>
    </div>
    <TournamentModal v-if="tournamentDetails" :visible="showModal" :tournament="tournamentDetails" @close="closeTournamentModal" />
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
