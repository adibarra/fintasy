<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue'

export default defineComponent({
  name: 'TournamentsList',
  props: {
    filters: Object,
  },
  setup(props) {
    const tournaments = ref(<tournament[]>); //I Know this is wrong, but working on it soon.
    const showModal = ref(false);
    const tournamentDetails = ref(null);
    const currentPage = ref(0);
    const totalPages = ref(1);
    const fintasy = useAPI();

    const fetchTournaments = async (page: number) => {
      const params = {
        owner: props.filters.uuidOwner,
        name: props.filters.name,
        status: props.filters.status,
        start_date: props.filters.dateTimeRange[0].toISOString(), // Convert start date to ISO string
        end_date: props.filters.dateTimeRange[1].toISOString(), // Convert end date to ISO string
        offset: (page - 1) * 10,
        limit: 10,
      }

      try {
        const response = await fintasy.getTournaments(params)
        if (response.success && response.data) {
          tournaments.value = response.data.items
          totalPages.value = response.data.totalPages
        }
        else {
          console.error('Failed to fetch tournaments:', response.message)
        }
      }
      catch (error) {
        console.error('Error fetching tournaments:', error)
      }
    }

    watch(() => props.filters, () => fetchTournaments(currentPage.value), { deep: true })

    onMounted(() => {
      fetchTournaments(currentPage.value)
    })

    const closeTournamentModal = () => {
      showModal.value = false;
    };

    const viewTournament = (uuid: string) => {
      console.log(`Viewing tournament ${uuid}`)
      const response = await fintasy.getTournament({ uuid });
      if (response.success && response.data) {
        tournamentDetails.value = response.data;
        showModal.value = true;
      } else {
        alert('Failed to load tournament details.'); // Or handle this error differently
      }
    }

    const joinTournament = (id: number) => {
      console.log(`Joining tournament ${id}`)
      // need logic for joining a tournament
      closeTournamentModal();
    }

    const changePage = (page: number) => {
      if (page < 1 || page > totalPages.value)
        return
      currentPage.value = page
      fetchTournaments(page)
    }

    onMounted(() => {
      fetchTournaments(1)
    })

    return {
      tournaments,
      currentPage,
      totalPages,
      viewTournament,
      joinTournament,
      changePage,
      showModal,
      tournamentDetails,
    }
  },
})
</script>

<template>
  <div class="tournaments-list">
    <div v-for="(tournament, index) in tournaments" :key="index" class="tournament-card">
      <h3>{{ tournament.name }}</h3>
      <p>{{ tournament.cost }}</p>
      <button @click="viewTournament(tournament.id)">
        View
      </button>
      <button @click="joinTournament(tournament.id)">
        Quick Join
      </button>
    </div>
    <button :disabled="currentPage <= 1" @click="changePage(currentPage - 1)">
      Prev
    </button>
    <button :disabled="currentPage >= totalPages" @click="changePage(currentPage + 1)">
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
