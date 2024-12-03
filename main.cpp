#include <iostream>
#include <vector>
#include <unordered_set>
#include <random>
#include <algorithm>
#include <chrono>

std::vector<int> solve_n_queens(int N) {
    std::mt19937 rng(std::random_device{}());
    std::vector<int> queens(N, -1);
    std::vector<std::unordered_set<int>> cols(N);
    std::vector<std::unordered_set<int>> diag1(2 * N - 1);
    std::vector<std::unordered_set<int>> diag2(2 * N - 1);
    std::unordered_set<int> conflicted_rows;

    auto initialize = [&]() {
        for (int row = 0; row < N; ++row) {
            int col = row;
            queens[row] = col;
            cols[col].insert(row);
            diag1[row + col].insert(row);
            diag2[row - col + N - 1].insert(row);
        }
        for (int row = 0; row < N; ++row) {
            int col = queens[row];
            int conflicts = cols[col].size() - 1
                + diag1[row + col].size() - 1
                + diag2[row - col + N - 1].size() - 1;
            if (conflicts > 0) {
                conflicted_rows.insert(row);
            }
        }
    };

    auto select_conflicted_queen = [&]() -> int {
        if (conflicted_rows.empty()) {
            return -1;
        }
        std::uniform_int_distribution<int> dist(0, conflicted_rows.size() - 1);
        auto it = conflicted_rows.begin();
        std::advance(it, dist(rng));
        return *it;
    };

    auto min_conflicts = [&](int row) {
        int min_conflicts = std::numeric_limits<int>::max();
        std::vector<int> min_cols;
        for (int col = 0; col < N; ++col) {
            int conflicts = cols[col].size() - (cols[col].count(row) ? 1 : 0)
                + diag1[row + col].size() - (diag1[row + col].count(row) ? 1 : 0)
                + diag2[row - col + N - 1].size() - (diag2[row - col + N - 1].count(row) ? 1 : 0);
            if (conflicts < min_conflicts) {
                min_conflicts = conflicts;
                min_cols.clear();
                min_cols.push_back(col);
            }
            else if (conflicts == min_conflicts) {
                min_cols.push_back(col);
            }
        }
        std::uniform_int_distribution<int> dist(0, min_cols.size() - 1);
        int new_col = min_cols[dist(rng)];
        int old_col = queens[row];

        cols[old_col].erase(row);
        diag1[row + old_col].erase(row);
        diag2[row - old_col + N - 1].erase(row);

        auto update_conflicts = [&](int col, int diag1_idx, int diag2_idx) {
            auto update_row_conflicts = [&](int r) {
                if (r != row) {
                    int conflicts = cols[queens[r]].size() - 1
                        + diag1[r + queens[r]].size() - 1
                        + diag2[r - queens[r] + N - 1].size() - 1;
                    if (conflicts > 0) {
                        conflicted_rows.insert(r);
                    }
                    else {
                        conflicted_rows.erase(r);
                    }
                }
            };
            for (int r : cols[col]) update_row_conflicts(r);
            for (int r : diag1[diag1_idx]) update_row_conflicts(r);
            for (int r : diag2[diag2_idx]) update_row_conflicts(r);
        };

        queens[row] = new_col;
        cols[new_col].insert(row);
        diag1[row + new_col].insert(row);
        diag2[row - new_col + N - 1].insert(row);

        update_conflicts(new_col, row + new_col, row - new_col + N - 1);

        int conflicts = cols[new_col].size() - 1
            + diag1[row + new_col].size() - 1
            + diag2[row - new_col + N - 1].size() - 1;
        if (conflicts > 0) {
            conflicted_rows.insert(row);
        }
        else {
            conflicted_rows.erase(row);
        }
    };

    initialize();
    int steps = 0;
    while (!conflicted_rows.empty()) {
        int row = select_conflicted_queen();
        if (row == -1) break;
        min_conflicts(row);
        steps++;
        if (steps % 1000 == 0) {
            std::cout << "Steps: " << steps << ", Conflicts: " << conflicted_rows.size() << std::endl;
        }
    }
    return queens;
}

bool is_valid_solution(const std::vector<int>& queens) {
    int N = queens.size();
    std::unordered_set<int> columns;
    std::unordered_set<int> diag1;
    std::unordered_set<int> diag2;

    for (int row = 0; row < N; ++row) {
        int col = queens[row];
        int d1 = row + col;
        int d2 = row - col;
        if (columns.count(col) > 0) {
            return false;
        }
        if (diag1.count(d1) > 0) {
            return false;
        }
        if (diag2.count(d2) > 0) {
            return false;
        }
        columns.insert(col);
        diag1.insert(d1);
        diag2.insert(d2);
    }
    return true;
}

int main() {
    int N = 10000;
    auto start_time = std::chrono::steady_clock::now();

    std::vector<int> solution = solve_n_queens(N);

    auto end_time = std::chrono::steady_clock::now();
    auto elapsed_ms = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();

    std::cout << "Solved N-Queens problem for N = " << N << " in " << elapsed_ms << " ms." << std::endl;

    bool is_valid = is_valid_solution(solution);
    if (is_valid) {
        std::cout << "The solution is valid." << std::endl;
    }
    else {
        std::cout << "The solution is invalid." << std::endl;
    }

    return 0;
}
