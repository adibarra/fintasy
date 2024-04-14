<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue'

export default defineComponent({
  name: 'TournamentsList',
  props: {
    filters: Object,
  },
  setup(props) {
    const tournaments = ref([])
    const currentPage = ref(1)
    const totalPages = ref(1)

    const fetchTournaments = async (page: number) => {
      // Placeholder for fetching logic
      // Here you would typically fetch from an API
      // For now, let's assume some static data
      tournaments.value = [
        { id: 1, name: 'Tournament A', cost: '100 Coins' },
        { id: 2, name: 'Tournament B', cost: '200 Coins' },
      ]
      totalPages.value = 5 // Example total pages
    }

    const viewTournament = (id: number) => {
      console.log(`Viewing tournament ${id}`)
      // Implement navigation or modal display
    }

    const joinTournament = (id: number) => {
      console.log(`Joining tournament ${id}`)
      // Add logic for joining a tournament
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
        Join
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
