import { shallowMount } from '@vue/test-utils'
import Dashboard from '@/views/Dashboard.vue'
import { createStore } from 'vuex'

describe('Dashboard.vue', () => {
  let store
  
  beforeEach(() => {
    store = createStore({
      state: {
        realtimeData: null,
        loading: false
      },
      actions: {
        fetchRealtimeData: jest.fn()
      }
    })
  })
  
  it('renders realtime data when loaded', () => {
    const wrapper = shallowMount(Dashboard, {
      global: {
        plugins: [store]
      }
    })
    
    expect(wrapper.find('.dashboard').exists()).toBe(true)
  })
  
  it('shows loading state', async () => {
    store.state.loading = true
    
    const wrapper = shallowMount(Dashboard, {
      global: {
        plugins: [store]
      }
    })
    
    expect(wrapper.find('.loading').exists()).toBe(true)
  })
}) 