#include <stdio.h>
#include <string.h>
#include <assert.h>
#define JEMALLOC_NO_DEMANGLE

#include "jemalloc/jemalloc.h"

// Compile with:
//
// JE_INSTALL_DIR=$(./je_install_dir.py)
// cc replace-hooks-test.c -I $JE_INSTALL_DIR/include -L $JE_INSTALL_DIR/lib -l jemalloc

static chunk_hooks_t old_hooks;

static void* chunk_alloc(void *new_addr, size_t size, size_t alignment, bool *zero, bool *commit, unsigned arena_ind) {
  printf("Entering chunk hook\n");
  return old_hooks.alloc(new_addr, size, alignment, zero, commit, arena_ind);
}

int main () {
  unsigned int arenas;
  size_t size = sizeof(unsigned int);
  // get the number of arenas
  assert(je_mallctl("arenas.narenas", &arenas, &size, NULL, 0) == 0);
  printf("There are %d arenas\n", (int)arenas);

  // grab a copy of the default chunk_hooks
  size = sizeof(chunk_hooks_t);
  assert(je_mallctl("arena.0.chunk_hooks", &old_hooks, &size, NULL, 0) == 0);

  // setup "new" hooks, old hooks but alloc calls new shim
  chunk_hooks_t new_hooks = old_hooks;
  new_hooks.alloc = chunk_alloc;

  // initialize all arenas with "thread.arena" call, then replace the chunk
  // hooks for all arenas, finally reset current "thread.arena" to 0
  unsigned arena;
  for (arena=0; arena<arenas; arena++) {
    char path[128];
    snprintf(path, sizeof(path), "arena.%u.chunk_hooks", arena);
    assert(je_mallctl("thread.arena", NULL, NULL, &arena, sizeof(arena)) == 0);
    assert(je_mallctl(path, NULL, NULL, &new_hooks, sizeof(chunk_hooks_t)) == 0);
  }
  arena = 0;
  assert(je_mallctl("thread.arena", NULL, NULL, &arena, sizeof(arena)) == 0);

  // make an allocation that'll require a new chunk
  printf("%p\n", chpl_je_malloc(100000000));
}
